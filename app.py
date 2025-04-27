import base64, io, os, socket, uuid, datetime as dt
from pathlib import Path
from typing import List
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageOps
import logging

# ------------------------------------------------------------- configuration
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.critical("OPENAI_API_KEY not set")
    raise SystemExit("OPENAI_API_KEY missing in environment")

client = OpenAI(api_key=api_key)

SAVE_DIR = Path("saved_images")
SAVE_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------- helpers
def nowstamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def save_bytes(img_bytes: bytes, ext: str) -> str:
    fname = f"{nowstamp()}-{uuid.uuid4().hex}.{ext}"
    (SAVE_DIR / fname).write_bytes(img_bytes)
    return f"/saved/{fname}"

def parse_int(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def normalize_name(name: str) -> str:
    name = name.lower()
    return name[:-4] + ".jpeg" if name.endswith(".jpg") else name

def b64_to_datauri(b64: str, ext: str) -> str:
    return f"data:image/{ext};base64,{b64}"

# ------------------------------------------------------------- Allowed kwargs builders
COMMON_ARGS_GEN = [  # /generate only – full set
    "size",
    "quality",
    "background",
    "output_format",
    "output_compression",
    "moderation",
]
# /edit must NEVER forward output_format, output_compression, moderation
COMMON_ARGS_EDIT = [
    "size",
    "quality",
    "background",
]

def build_kwargs(src, *, for_generate=False):
    kw = {}
    allowed = COMMON_ARGS_GEN if for_generate else COMMON_ARGS_EDIT
    for k in allowed:
        v = src.get(k)
        if v not in (None, "", "auto"):
            kw[k] = int(v) if k == "output_compression" else v
    return kw

# ------------------------------------------------------------- validation helpers
MAX_IMAGE_BYTES = 25 * 1024 * 1024  # 25 MB

def validate_transparency(fmt: str, background: str):
    if background == "transparent" and fmt not in ("png", "webp"):
        raise ValueError("background=transparent is allowed only with png or webp output_format")

def validate_n(n: int):
    if not 1 <= n <= 8:
        raise ValueError("n must be between 1 and 8 inclusive")

def _pil_open_clone(buf: io.BytesIO):
    p = Image.open(buf)
    p.load()
    return p

def _auto_rgba_mask(grab: Image.Image) -> io.BytesIO:
    """Return a PNG mask: transparent on border pixels (alpha==0), black opaque elsewhere."""
    if grab.mode != "RGBA":
        grab = grab.convert("RGBA")
    alpha = grab.split()[-1]
    w, h = grab.size
    mask = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    # Create transparency where alpha==0
    mask_data = [
        (0, 0, 0, 0) if a == 0 else (0, 0, 0, 255)
        for a in alpha.getdata()
    ]
    mask.putdata(mask_data)
    out = io.BytesIO()
    mask.save(out, format="PNG")
    out.name = "auto_outpaint_mask.png"
    out.seek(0)
    return out

def _ensure_mask_valid(mask_buf: io.BytesIO, expected_size):
    mask = _pil_open_clone(mask_buf)
    if mask.format != "PNG":
        raise ValueError("Mask must be a PNG file")
    if mask.size != expected_size:
        raise ValueError("Mask dimensions must match reference image dimensions")
    if "A" not in mask.mode:
        # Auto‑convert per docs
        logger.info("Mask missing alpha channel – auto‑converting to RGBA with alpha from grayscale")
        mask = mask.convert("L")  # grayscale
        rgba = mask.convert("RGBA")
        rgba.putalpha(mask)
        tmp = io.BytesIO()
        rgba.save(tmp, format="PNG")
        tmp.name = "mask_alpha.png"
        tmp.seek(0)
        return tmp
    mask_buf.seek(0)
    return mask_buf

def _validate_reference_images(images: List[io.BytesIO]):
    sizes = []
    for buf in images:
        # size check
        buf.seek(0, os.SEEK_END)
        if buf.tell() > MAX_IMAGE_BYTES:
            raise ValueError("Each reference image must be ≤ 25 MB")
        buf.seek(0)
        im = _pil_open_clone(buf)
        if im.mode not in ("RGB", "RGBA"):
            raise ValueError("Reference images must be RGB or RGBA")
        sizes.append(im.size)
    if len({s for s in sizes}) > 1:
        raise ValueError("All reference images must have identical width × height")
    return sizes[0]

# ------------------------------------------------------------- flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saved/<path:fname>")
def serve_saved(fname):
    return send_from_directory(SAVE_DIR, fname, as_attachment=False)

# ============================================================= /generate
@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    fmt = data.get("output_format", "png") or "png"
    background = data.get("background", "")
    try:
        validate_transparency(fmt, background)
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

    try:
        n = parse_int(data.get("n", 1))
        validate_n(n)
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=n,
            **build_kwargs(data, for_generate=True),
        )
        data_uris, urls = [], []
        for item in result.data:
            b64 = item.b64_json
            img_bytes = base64.b64decode(b64)
            data_uris.append(b64_to_datauri(b64, fmt))
            urls.append(save_bytes(img_bytes, fmt))
        return jsonify(ok=True, data_uris=data_uris, urls=urls)
    except Exception as e:
        logger.exception("Generate failed")
        return jsonify(ok=False, error=str(e)), 500

# ============================================================= /edit
@app.route("/edit", methods=["POST"])
def edit():
    data = request.form
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    # ---- gather reference images ----
    images: List[io.BytesIO] = []
    for i in range(1, 11):
        f = request.files.get(f"image{i}")
        if f and f.filename:
            buf = io.BytesIO(f.read())
            buf.name = normalize_name(f.filename)
            buf.seek(0)
            images.append(buf)
    if not images:
        return jsonify(ok=False, error="At least one reference image required"), 400

    # Validation of ref images
    try:
        first_size = _validate_reference_images(images)
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

    # ---- mask handling ----
    mask_file = None
    f_mask = request.files.get("mask")
    if f_mask and f_mask.filename:
        buf = io.BytesIO(f_mask.read())
        buf.name = "mask.png"
        buf.seek(0)
        try:
            mask_file = _ensure_mask_valid(buf, first_size)
        except ValueError as e:
            return jsonify(ok=False, error=str(e)), 400

    # ---- auto‑mask for out‑paint (single expanded PNG named outpaint.*) ----
    if not mask_file and len(images) == 1 and images[0].name.startswith("outpaint"):
        try:
            mask_file = _auto_rgba_mask(_pil_open_clone(images[0]))
            logger.info("Auto‑generated out‑paint mask attached")
        except Exception:
            logger.warning("Auto‑mask generation failed; proceeding without mask")
            mask_file = None

    # ---- build kwargs & call API ----
    kwargs = build_kwargs(data)
    if mask_file:
        kwargs["mask"] = mask_file

    # Optional n param – include only if user supplied and valid
    try:
        n_val = data.get("n")
        if n_val:
            n_edit = parse_int(n_val)
            validate_n(n_edit)
            kwargs["n"] = n_edit  # Only forwarded if valid
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400

    try:
        result = client.images.edit(
            model="gpt-image-1",
            prompt=prompt,
            image=images,
            **kwargs,
        )
        # API always returns same format as first image
        returned_fmt = images[0].name.rsplit(".", 1)[-1]
        b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(b64)
        url = save_bytes(img_bytes, returned_fmt)
        return jsonify(ok=True, data_uri=b64_to_datauri(b64, returned_fmt), url=url)
    except Exception as e:
        logger.exception("Edit failed")
        return jsonify(ok=False, error=str(e)), 500

# ------------------------------------------------------------- utils

def find_free_port(start_port=5000, max_tries=100):
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("No free ports found in range.")

if __name__ == "__main__":
    port = find_free_port(5000)
    print(f"Starting Flask on port {port}")
    app.run(debug=True, port=port)