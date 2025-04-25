import base64, io, os, uuid, datetime as dt
from pathlib import Path
from typing import List
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
import logging

# ------------------------------------------------------------- configuration
# Configure logging with proper error handling
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)
load_dotenv()                                                # reads .env
# Initialize OpenAI client with error handling
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.critical(f"Failed to initialize OpenAI client: {e}")
    raise

SAVE_DIR = Path("saved_images")
SAVE_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------- helpers
def nowstamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")

def save_bytes(img_bytes: bytes, ext: str) -> str:
    fname = f"{nowstamp()}-{uuid.uuid4().hex}.{ext}"
    (SAVE_DIR / fname).write_bytes(img_bytes)
    return f"/saved/{fname}"

def file_to_bytes(f):
    return f.read() if f and f.filename else None

def b64_to_datauri(b64: str, ext="png") -> str:
    return f"data:image/{ext};base64,{b64}"

def parse_int(value, default=1):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default

# ------------------------------------------------------------- Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saved/<path:fname>")
def serve_saved(fname):
    return send_from_directory(SAVE_DIR, fname, as_attachment=False)

# ------------------------------------------------------------- routes
COMMON_ARGS = ["size", "quality", "background", "output_format",
               "output_compression", "moderation"]

def build_kwargs(src):
    """Translate HTML form → kwargs understood by the Image API."""
    kw = {}
    for k in COMMON_ARGS:
        v = src.get(k)
        if v not in (None, "", "auto"):
            kw[k if k != "output_format" else "output_format"] = v
    if "output_compression" in kw:
        kw["output_compression"] = int(kw["output_compression"])
    return kw

@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    prompt = data.get("prompt", "").strip()
    n      = parse_int(data.get("n", 1), 1)

    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required"}), 400

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=n,
            **build_kwargs(data),
        )
        fmt = data.get("output_format", "png")
        data_uris, urls = [], []
        for item in result.data:
            b64 = item.b64_json
            img_bytes = base64.b64decode(b64)
            data_uris.append(b64_to_datauri(b64, fmt))
            urls.append(save_bytes(img_bytes, fmt))
        return jsonify({"ok": True, "data_uris": data_uris, "urls": urls})
    except Exception as e:
        logger.exception("Generate failed")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/edit", methods=["POST"])
def edit():
    data = request.form
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"ok": False, "error": "Prompt is required"}), 400

    # collect up to 10 images: fields image1 … image10
    images: List[io.BytesIO] = []
    for i in range(1, 11):
        b = file_to_bytes(request.files.get(f"image{i}"))
        if b: images.append(io.BytesIO(b))
    if not images:
        return jsonify({"ok": False, "error": "At least one image required"}), 400

    mask_bytes = file_to_bytes(request.files.get("mask"))
    mask_file  = io.BytesIO(mask_bytes) if mask_bytes else None

    try:
        result = client.images.edit(
            model="gpt-image-1",
            prompt=prompt,
            image=images,
            mask=mask_file,
            **build_kwargs(data),
        )
        fmt = data.get("output_format", "png")
        b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(b64)
        url = save_bytes(img_bytes, fmt)
        return jsonify({"ok": True,
                        "data_uri": b64_to_datauri(b64, fmt),
                        "url": url})
    except Exception as e:
        logger.exception("Edit failed")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
