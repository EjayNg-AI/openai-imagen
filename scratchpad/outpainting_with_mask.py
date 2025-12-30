import base64
import datetime as dt
import io
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file, send_from_directory
from openai import OpenAI
from PIL import Image

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY missing in environment")

client = OpenAI(api_key=api_key)

SAVE_DIR = Path("saved_images")
SAVE_DIR.mkdir(exist_ok=True)

HTML_PATH = Path(__file__).resolve().parent / "outpainting_with_mask.html"

ALLOWED_SIZES = {
    "1024x1024": (1024, 1024),
    "1536x1024": (1536, 1024),
    "1024x1536": (1024, 1536),
}
MAX_IMAGE_BYTES = 25 * 1024 * 1024
MAX_MASK_BYTES = 4_000_000


def nowstamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def save_bytes(img_bytes: bytes, ext: str) -> str:
    fname = f"{nowstamp()}-{uuid.uuid4().hex}.{ext}"
    (SAVE_DIR / fname).write_bytes(img_bytes)
    return f"/saved/{fname}"


def normalize_name(name: str) -> str:
    name = name.lower()
    return name[:-4] + ".jpeg" if name.endswith(".jpg") else name


def b64_to_datauri(b64: str, ext: str) -> str:
    return f"data:image/{ext};base64,{b64}"


def _buffer_size(buf: io.BytesIO) -> int:
    buf.seek(0, os.SEEK_END)
    size = buf.tell()
    buf.seek(0)
    return size


def _pil_open_clone(buf: io.BytesIO) -> Image.Image:
    img = Image.open(buf)
    img.load()
    return img


def _read_upload(field_name: str):
    f = request.files.get(field_name)
    if not f or not f.filename:
        return None
    buf = io.BytesIO(f.read())
    buf.name = normalize_name(f.filename)
    buf.seek(0)
    return buf


def _validate_canvas_image(buf: io.BytesIO, expected_size=None) -> Image.Image:
    if _buffer_size(buf) > MAX_IMAGE_BYTES:
        raise ValueError("Image must be 25MB or smaller")

    img = _pil_open_clone(buf)
    if img.mode not in ("RGB", "RGBA"):
        raise ValueError("Image must be RGB or RGBA")

    if img.format not in ("PNG", "JPEG", "WEBP"):
        raise ValueError("Canvas image must be PNG, JPEG, or WEBP")

    if expected_size and img.size != expected_size:
        raise ValueError("Canvas image size must match the selected canvas size")

    buf.seek(0)
    return img


def _validate_mask(buf: io.BytesIO, expected_size) -> None:
    if _buffer_size(buf) >= MAX_MASK_BYTES:
        raise ValueError("Mask must be smaller than 4,000,000 bytes")

    mask = _pil_open_clone(buf)
    if mask.format != "PNG":
        raise ValueError("Mask must be a PNG file")

    if mask.size != expected_size:
        raise ValueError("Mask size must match the selected canvas size")

    if "A" not in mask.mode:
        raise ValueError("Mask must include an alpha channel")

    buf.seek(0)


def _parse_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _validate_n(value):
    if value is None:
        return None
    if not 1 <= value <= 8:
        raise ValueError("n must be between 1 and 8")
    return value


app = Flask(__name__)


@app.get("/")
def serve_frontend():
    if HTML_PATH.exists():
        return send_file(HTML_PATH)
    return ("outpainting_with_mask.html is missing", 404)


@app.get("/saved/<path:fname>")
def serve_saved(fname: str):
    return send_from_directory(SAVE_DIR, fname, as_attachment=False)


@app.post("/edit")
def edit():
    data = request.form
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    mode = (data.get("mode") or "standard").strip().lower()
    outpaint = mode == "outpaint"

    size_val = (data.get("size") or "").strip()
    expected_size = None

    try:
        n_val = _validate_n(_parse_int(data.get("n")))
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    if outpaint:
        if size_val not in ALLOWED_SIZES:
            return (
                jsonify(
                    ok=False,
                    error="Outpaint requires a fixed canvas size (1024x1024, 1536x1024, 1024x1536)",
                ),
                400,
            )
        expected_size = ALLOWED_SIZES[size_val]

    image_buf = _read_upload("image")
    if not image_buf:
        return jsonify(ok=False, error="Image is required"), 400

    try:
        _validate_canvas_image(image_buf, expected_size=expected_size)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    mask_buf = None
    if outpaint:
        mask_buf = _read_upload("mask")
        if not mask_buf:
            return jsonify(ok=False, error="Mask is required for outpainting"), 400
        try:
            _validate_mask(mask_buf, expected_size)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400

        image_w = _parse_int(data.get("image_w"))
        image_h = _parse_int(data.get("image_h"))
        pos_x = _parse_int(data.get("pos_x"))
        pos_y = _parse_int(data.get("pos_y"))
        canvas_w = _parse_int(data.get("canvas_w"))
        canvas_h = _parse_int(data.get("canvas_h"))

        if None not in (image_w, image_h, pos_x, pos_y, canvas_w, canvas_h):
            if (canvas_w, canvas_h) != expected_size:
                return jsonify(ok=False, error="Canvas size metadata mismatch"), 400
            if image_w > canvas_w or image_h > canvas_h:
                return jsonify(ok=False, error="Image does not fit within the canvas"), 400
            if pos_x < 0 or pos_y < 0:
                return jsonify(ok=False, error="Image position must be inside the canvas"), 400
            if pos_x + image_w > canvas_w or pos_y + image_h > canvas_h:
                return jsonify(ok=False, error="Image position must stay inside the canvas"), 400

    kwargs = {}
    if outpaint:
        kwargs["size"] = size_val
        kwargs["background"] = "auto"
        kwargs["output_format"] = "png"
    else:
        if size_val and size_val != "auto":
            if size_val not in ALLOWED_SIZES:
                return jsonify(ok=False, error="Invalid size"), 400
            kwargs["size"] = size_val
    if n_val is not None:
        kwargs["n"] = n_val

    request_kwargs = {
        "model": "gpt-image-1.5",
        "prompt": prompt,
        "image": image_buf,
        **kwargs,
    }
    if mask_buf:
        request_kwargs["mask"] = mask_buf

    try:
        result = client.images.edit(**request_kwargs)
    except Exception as exc:
        return jsonify(ok=False, error=str(exc)), 500

    out_ext = "png"
    if not outpaint:
        name = image_buf.name or ""
        if "." in name:
            out_ext = normalize_name(name).rsplit(".", 1)[-1]

    data_uris, urls = [], []
    for item in result.data:
        b64 = item.b64_json
        img_bytes = base64.b64decode(b64)
        data_uris.append(b64_to_datauri(b64, out_ext))
        urls.append(save_bytes(img_bytes, out_ext))

    return jsonify(ok=True, data_uris=data_uris, urls=urls)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
