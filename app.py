import base64
import socket
import io
import os
import uuid
import datetime as dt
from pathlib import Path
from typing import List

from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
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
        return max(1, int(value))
    except (TypeError, ValueError):
        return default

def normalize_name(name: str) -> str:
    name = name.lower()
    return name[:-4] + ".jpeg" if name.endswith(".jpg") else name

def b64_to_datauri(b64: str, ext: str) -> str:
    return f"data:image/{ext};base64,{b64}"

# ------------------------------------------------------------- flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saved/<path:fname>")
def serve_saved(fname):
    return send_from_directory(SAVE_DIR, fname, as_attachment=False)

# ------------------------------------------------------------- arg helpers
COMMON_ARGS_GEN = [
    "size",
    "quality",
    "background",
    "output_format",
    "output_compression",
    "moderation",
]
# NOTE: images.edit **does NOT** accept output_format; leave it out.
COMMON_ARGS_EDIT = [
    "size",
    "quality",
    "background",
    "output_compression",
    "moderation",
]

def build_kwargs(src, for_generate=False):
    kw = {}
    allowed = COMMON_ARGS_GEN if for_generate else COMMON_ARGS_EDIT
    for k in allowed:
        v = src.get(k)
        if v not in (None, "", "auto"):
            kw[k] = int(v) if k == "output_compression" else v
    return kw

# ------------------------------------------------------------- routes
@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    prompt = data.get("prompt", "").strip()
    n = parse_int(data.get("n", 1), 1)
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=n,
            **build_kwargs(data, for_generate=True),
        )
        fmt = data.get("output_format", "png")
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

@app.route("/edit", methods=["POST"])
def edit():
    data = request.form
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify(ok=False, error="Prompt is required"), 400

    # ---- collect images ----
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

    # ---- optional mask ----
    mask_file = None
    f_mask = request.files.get("mask")
    if f_mask and f_mask.filename:
        buf = io.BytesIO(f_mask.read())
        buf.name = "mask.png"
        buf.seek(0)
        mask_file = buf

    try:
        kwargs = build_kwargs(data)
        if mask_file:
            kwargs["mask"] = mask_file

        result = client.images.edit(
            model="gpt-image-1",
            prompt=prompt,
            image=images,
            **kwargs,
        )

        returned_fmt = images[0].name.rsplit(".", 1)[-1]
        b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(b64)
        url = save_bytes(img_bytes, returned_fmt)
        return jsonify(ok=True, data_uri=b64_to_datauri(b64, returned_fmt), url=url)
    except Exception as e:
        logger.exception("Edit failed")
        return jsonify(ok=False, error=str(e)), 500




def find_free_port(start_port=5000, max_tries=100):
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("No free ports found in range.")


if __name__ == "__main__":
    port = find_free_port(5000)
    print(f"Starting Flask on port {port}")
    app.run(debug=True, port=port)


