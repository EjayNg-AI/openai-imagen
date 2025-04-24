````markdown
# OpenAI Image-API Playground (Flask Edition)

This repository is a **personal, single-user test bed** for experimenting with OpenAI’s new `gpt-image-1` endpoints—**_not_** a production-grade service.  
It demonstrates only the core “generate” and “edit” flows and a couple of persistence options.

---

## Quick start

```bash
git clone <this-repo>
cd image-playground

# 1 — set up Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2 — create .env with your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# 3 — run
python app.py
# open http://127.0.0.1:5000
```
````

Generated or edited images are:

- **previewed in-browser** via a data-URI
- **saved on disk** under `saved_images/` and served at `/saved/<filename>`
- **downloadable** client-side with one click

---

## What this project **is**

- A concise, readable reference for hitting `images.generate` and `images.edit` from Flask
- A sandbox for tweaking prompts, image sizes, quality settings, etc.
- A stepping-stone to bigger things—queues, auth, masking UI, cloud storage…

## What it **is _not_** (yet)

- Hardened for multiple users, rate-limits, or untrusted input
- Equipped with background workers, robust error handling, or cost tracking
- A polished front-end—just enough HTML/CSS/JS to prove the calls work

---

## Next steps (ideas)

- Mask upload / paint-in-browser for inpainting
- React / Next.js front-end & API gateway
- Worker queue (Celery / RQ) to avoid blocking Flask
- S3 (or MinIO) storage and signed download links
