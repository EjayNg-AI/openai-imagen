import base64, io, os, uuid, datetime as dt
from pathlib import Path
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv

# ------------------------------------------------------------------ configuration
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
SAVE_DIR.mkdir(exist_ok=True)                                # local persistence folder

# ------------------------------------------------------------------ helpers
def file_to_bytes(f):
    return f.read() if f and f.filename else None


def b64_to_datauri(b64, fmt="png"):
    return f"data:image/{fmt};base64,{b64}"


def save_image_bytes(img_bytes: bytes, fmt: str) -> str:
    """Write image to disk, return the relative URL for accessing it."""
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"{stamp}-{uuid.uuid4().hex}.{fmt}"
    (SAVE_DIR / fname).write_bytes(img_bytes)
    return f"/saved/{fname}"


# ------------------------------------------------------------------ Flask app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/saved/<path:filename>")
def saved_file(filename):
    """Serve persisted images."""
    return send_from_directory(SAVE_DIR, filename, as_attachment=False)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    prompt = data.get("prompt", "").strip()
    size = data.get("size", "1024x1024")
    quality = data.get("quality", "auto")
    bg = data.get("background", None)
    fmt = data.get("format", "png")
    n = int(data.get("n", 1))

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            quality=quality,
            background=bg,
            output_format=fmt,
            n=n,
        )
        img_b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(img_b64)
        url = save_image_bytes(img_bytes, fmt)
        return jsonify(
            {"ok": True, "data_uri": b64_to_datauri(img_b64, fmt), "url": url}
        )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/edit", methods=["POST"])
def edit():
    data = request.form
    prompt = data.get("prompt", "").strip()
    size = data.get("size", "1024x1024")

    img1_bytes = file_to_bytes(request.files.get("image1"))
    img2_bytes = file_to_bytes(request.files.get("image2"))

    if not prompt or not img1_bytes:
        return (
            jsonify({"ok": False, "error": "Need prompt + at least 1 image"}),
            400,
        )

    try:
        image_files = [io.BytesIO(img1_bytes)]
        if img2_bytes:
            image_files.append(io.BytesIO(img2_bytes))

        result = client.images.edit(
            model="gpt-image-1", image=image_files, prompt=prompt, size=size
        )
        img_b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(img_b64)
        url = save_image_bytes(img_bytes, "png")
        return jsonify(
            {"ok": True, "data_uri": b64_to_datauri(img_b64), "url": url}
        )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
