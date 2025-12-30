import base64, io, os, socket, uuid, datetime as dt
from pathlib import Path
from typing import List
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image, ImageOps
from werkzeug.exceptions import HTTPException
import logging

# ------------------------------------------------------------- configuration
ROOT_DIR = Path(__file__).resolve().parent
LOG_FILE = ROOT_DIR / "app.log"
ERROR_LOG_FILE = ROOT_DIR / "error.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"

def _has_file_handler(logger_obj: logging.Logger, path: Path) -> bool:
    target = path.resolve()
    for handler in logger_obj.handlers:
        if isinstance(handler, logging.FileHandler):
            try:
                if Path(handler.baseFilename).resolve() == target:
                    return True
            except Exception:
                continue
    return False

def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)

    if not _has_file_handler(root, LOG_FILE):
        handler = logging.FileHandler(LOG_FILE)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        root.addHandler(handler)

    if not _has_file_handler(root, ERROR_LOG_FILE):
        err_handler = logging.FileHandler(ERROR_LOG_FILE)
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
        root.addHandler(err_handler)

configure_logging()
logger = logging.getLogger(__name__)

def _close_log_file_handlers():
    root = logging.getLogger()
    targets = {LOG_FILE.resolve(), ERROR_LOG_FILE.resolve()}
    for handler in list(root.handlers):
        if isinstance(handler, logging.FileHandler):
            try:
                handler_path = Path(handler.baseFilename).resolve()
            except Exception:
                continue
            if handler_path in targets:
                try:
                    handler.flush()
                finally:
                    handler.close()
                root.removeHandler(handler)

def _trim_log_file(path: Path, max_lines=200, keep_lines=100):
    try:
        if not path.exists():
            return
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines(
            keepends=True
        )
        if len(lines) <= max_lines:
            return
        path.write_text("".join(lines[-keep_lines:]), encoding="utf-8")
    except Exception:
        # Avoid raising during request finalizers.
        pass

def trim_log_files():
    _close_log_file_handlers()
    _trim_log_file(LOG_FILE)
    _trim_log_file(ERROR_LOG_FILE)
    configure_logging()

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

def detect_image_ext(img_bytes: bytes) -> str | None:
    try:
        with Image.open(io.BytesIO(img_bytes)) as im:
            fmt = (im.format or "").lower()
    except Exception:
        return None
    if fmt == "jpg":
        fmt = "jpeg"
    return fmt if fmt in ("png", "jpeg", "webp") else None

def log_request_exception(message: str):
    try:
        form_keys = sorted(request.form.keys())
        file_names = {
            key: f.filename
            for key, f in request.files.items()
            if f and f.filename
        }
        logger.exception(
            "%s | path=%s method=%s remote=%s form_keys=%s files=%s",
            message,
            request.path,
            request.method,
            request.remote_addr,
            form_keys,
            file_names,
        )
    except Exception:
        logger.exception("%s (failed to capture request context)", message)

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
# (outpaint mode sets output_format explicitly server-side)
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
MAX_OUTPAINT_MASK_BYTES = 4_000_000
OUTPAINT_CANVAS_SIZES = {
    "1024x1024": (1024, 1024),
    "1536x1024": (1536, 1024),
    "1024x1536": (1024, 1536),
}
OUTPAINT_CANVAS_FORMATS = {"PNG", "JPEG", "WEBP"}

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

def _buffer_size(buf: io.BytesIO) -> int:
    buf.seek(0, os.SEEK_END)
    size = buf.tell()
    buf.seek(0)
    return size

def _parse_outpaint_size(value: str):
    return OUTPAINT_CANVAS_SIZES.get(value)

def _ensure_outpaint_mask_valid(mask_buf: io.BytesIO, expected_size):
    if _buffer_size(mask_buf) >= MAX_OUTPAINT_MASK_BYTES:
        raise ValueError("Mask must be smaller than 4,000,000 bytes")
    mask = _pil_open_clone(mask_buf)
    if mask.format != "PNG":
        raise ValueError("Mask must be a PNG file")
    if mask.size != expected_size:
        raise ValueError("Mask dimensions must match the selected canvas size")
    if "A" not in mask.mode:
        raise ValueError("Mask must include an alpha channel")
    alpha = mask.getchannel("A")
    if not set(alpha.getdata()).issubset({0, 255}):
        raise ValueError("Mask alpha must be fully transparent (0) or fully opaque (255)")
    mask_buf.seek(0)
    return mask_buf

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

@app.errorhandler(Exception)
def handle_unexpected_error(err):
    if isinstance(err, HTTPException):
        level = logging.ERROR if err.code and err.code >= 500 else logging.WARNING
        logger.log(
            level,
            "HTTP %s: %s | path=%s method=%s remote=%s",
            err.code,
            err.description,
            request.path,
            request.method,
            request.remote_addr,
        )
        if request.path in ("/generate", "/edit"):
            return jsonify(ok=False, error=err.description), err.code or 500
        return err
    log_request_exception("Unhandled exception")
    return jsonify(ok=False, error="Internal server error"), 500

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
            model="gpt-image-1.5",
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
        log_request_exception("Generate failed")
        return jsonify(ok=False, error=str(e)), 500
    finally:
        trim_log_files()

# ============================================================= /edit
@app.route("/edit", methods=["POST"])
def edit():
    data = request.form
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    mode = (data.get("edit_mode") or data.get("mode") or "").strip().lower()
    outpaint = mode == "outpaint"
    outpaint_size = (data.get("size") or "").strip()
    expected_size = _parse_outpaint_size(outpaint_size) if outpaint else None
    if outpaint and not expected_size:
        return (
            jsonify(
                ok=False,
                error="Outpaint requires a fixed canvas size (1024x1024, 1536x1024, 1024x1536)",
            ),
            400,
        )

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
        msg = (
            "Outpaint requires exactly one reference image"
            if outpaint
            else "At least one reference image required"
        )
        return jsonify(ok=False, error=msg), 400
    if outpaint and len(images) != 1:
        return jsonify(ok=False, error="Outpaint requires exactly one reference image"), 400

    # Validation of ref images
    try:
        first_size = _validate_reference_images(images)
    except ValueError as e:
        return jsonify(ok=False, error=str(e)), 400
    if outpaint:
        if first_size != expected_size:
            return (
                jsonify(
                    ok=False,
                    error="Canvas size must match the selected outpaint size",
                ),
                400,
            )
        try:
            canvas_img = _pil_open_clone(images[0])
        except Exception:
            return jsonify(ok=False, error="Failed to read outpaint canvas"), 400
        if canvas_img.format not in OUTPAINT_CANVAS_FORMATS:
            return jsonify(
                ok=False, error="Canvas image must be PNG, JPEG, or WEBP"
            ), 400
        images[0].seek(0)

    # ---- mask handling ----
    mask_file = None
    f_mask = request.files.get("mask")
    if outpaint:
        if not f_mask or not f_mask.filename:
            return jsonify(ok=False, error="Mask is required for outpainting"), 400
        buf = io.BytesIO(f_mask.read())
        buf.name = "mask.png"
        buf.seek(0)
        try:
            mask_file = _ensure_outpaint_mask_valid(buf, expected_size)
        except ValueError as e:
            return jsonify(ok=False, error=str(e)), 400
    else:
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

    if outpaint:
        image_w = parse_int(data.get("image_w"), default=None)
        image_h = parse_int(data.get("image_h"), default=None)
        pos_x = parse_int(data.get("pos_x"), default=None)
        pos_y = parse_int(data.get("pos_y"), default=None)
        canvas_w = parse_int(data.get("canvas_w"), default=None)
        canvas_h = parse_int(data.get("canvas_h"), default=None)
        if None not in (image_w, image_h, pos_x, pos_y, canvas_w, canvas_h):
            if (canvas_w, canvas_h) != expected_size:
                return jsonify(ok=False, error="Canvas metadata mismatch"), 400
            if image_w > canvas_w or image_h > canvas_h:
                return jsonify(ok=False, error="Image does not fit within the canvas"), 400
            if pos_x < 0 or pos_y < 0:
                return jsonify(ok=False, error="Image position must be inside the canvas"), 400
            if pos_x + image_w > canvas_w or pos_y + image_h > canvas_h:
                return jsonify(ok=False, error="Image position must stay inside the canvas"), 400

    # ---- build kwargs & call API ----
    kwargs = build_kwargs(data)
    if outpaint:
        kwargs["size"] = outpaint_size
        kwargs["background"] = "auto"
        kwargs["output_format"] = "png"
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
            model="gpt-image-1.5",
            prompt=prompt,
            image=images,
            **kwargs,
        )
        # API always returns same format as first image
        if outpaint:
            returned_fmt = "png"
        else:
            returned_fmt = (
                images[0].name.rsplit(".", 1)[-1]
                if "." in images[0].name
                else "png"
            )
        data_uris, urls = [], []
        for item in result.data:
            b64 = item.b64_json
            img_bytes = base64.b64decode(b64)
            actual_fmt = detect_image_ext(img_bytes) or returned_fmt
            data_uris.append(b64_to_datauri(b64, actual_fmt))
            urls.append(save_bytes(img_bytes, actual_fmt))
        if len(data_uris) == 1:
            return jsonify(ok=True, data_uri=data_uris[0], url=urls[0])
        return jsonify(ok=True, data_uris=data_uris, urls=urls)
    except Exception as e:
        log_request_exception("Edit failed")
        return jsonify(ok=False, error=str(e)), 500
    finally:
        trim_log_files()

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
