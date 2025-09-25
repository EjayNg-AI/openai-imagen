# OpenAI Image-API Playground (Flask Edition)

This repository is a **personal, single-user test bed** for experimenting with OpenAI’s new `gpt-image-1` endpoints—**_not_** a production-grade service.  
It demonstrates only the core “generate” and “edit” flows and a couple of persistence options.

---

## Quick start

```bash
git clone git@github.com:EjayNg-AI/openai-imagen.git
cd openai-imagen

# 1 — set up Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2 — create .env with your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# 3 — run
python app.py
# open http://127.0.0.1:5000
```

## Overview of functionalities

Generated or edited images are:

- **previewed in-browser** via a data-URI
- **saved on disk** under `saved_images/` and served at `/saved/<filename>`
- **downloadable** client-side with one click
- **styled in dark mode** across both the main playground (`templates/index.html`) and the scratchpad UI, giving consistent contrast against the new palette.

### Responses playground (scratchpad)

In addition to the image endpoints, the repository now ships with a mini **Responses API playground** hosted from `scratchpad/examplecode.py`:

- Run `python scratchpad/examplecode.py` to start a lightweight Flask server (defaults to `http://127.0.0.1:2357`).
- The root path serves `scratchpad/try.html`, a dark-themed frontend with developer/user textareas (1000-word limit each) and live word counts.
- Submissions POST to `/api/responses`, which forwards the request to `OpenAI.responses.create` using the same schema enforced in code.
- The backend response is returned verbatim *and* pre-parsed: the server extracts the five paragraph strings from the JSON payload and exposes them separately in the JSON reply.
- The UI renders both the raw response (pretty-printed JSON) and the cleaned paragraphs in a dedicated high-contrast textbox for quick reading.

---

## Current capabilities in detail

The test-bed supports every documented knob in the **OpenAI Image API**:

| Feature                | Usage in HTML/JS                  | Flask param → API arg                   |
| ---------------------- | --------------------------------- | --------------------------------------- |
| Multiple results (`n`) | _Generate_ → **Number (n)** field | `n`                                     |
| Up to 10 ref images    | _Edit_ → “+ add image” button     | `image=[…]`                             |
| Alpha-mask inpainting  | _Edit_ → **Mask** file input      | `mask=`                                 |
| Quality                | _Quality_ dropdowns               | `quality=`                              |
| Sizes                  | _Size_ dropdowns                  | `size=`                                 |
| Transparent background | _Background_ = `transparent`      | `background=`                           |
| Formats/compression    | _Format_ + slider                 | `output_format=`, `output_compression=` |
| Moderation strictness  | _Moderation_ dropdown             | `moderation=`                           |

All returned images are base-64 decoded, persisted to `saved_images/`, and exposed at  
`/saved/<file>` for easy sharing.

---

## What this project **is**

- A concise, readable reference for hitting `images.generate` and `images.edit` from Flask
- A sibling playground for experimenting with the `responses.create` endpoint, including schema validation and result extraction
- A sandbox for tweaking prompts, image sizes, quality settings, etc.
- A stepping-stone to bigger things—queues, auth, masking UI, cloud storage…

---

## What it **is _not_** (yet)

- Hardened for multiple users, rate-limits, or untrusted input
- Equipped with background workers, robust error handling, or cost tracking
- A polished front-end—just enough HTML/CSS/JS to prove the calls work

---

## Next steps (ideas)

- React / Next.js front-end & API gateway
- Worker queue (Celery / RQ) to avoid blocking Flask
- S3 (or MinIO) storage and signed download links
- Broaden the responses playground into a reusable SDK demo or QA harness
