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

### Playgrounds

- **Image playground** (run `python app.py`): dark-mode UI at `http://127.0.0.1:5000` for `images.generate` and `images.edit`. It validates prompts/background/format, saves returned images under `saved_images/`, and exposes both previews and saved URLs.
- **Responses playground** (run `python scratchpad/examplecode.py` → `http://127.0.0.1:2357`):
  - `try.html` posts `{developer_message, user_message}` to `/api/responses`, which calls `responses.create` with a strict five-paragraph JSON schema. The backend extracts the paragraphs and returns them alongside the raw model dump; the UI pretty-prints both.
  - `prompt_runner.html` builds multi-turn conversations (developer/user/assistant rows) and POSTs `{messages:[...]}` to `/api/prompt-run`. The backend normalizes the array and forwards it to `responses.create` with text output + web search enabled. The UI shows only the assistant output, plus a “Last sent payload” box (with copy buttons) that reflects the exact parameters sent to OpenAI. System-message loader buttons pull sections from `scratchpad/system_messages_consolidated.md` via `/api/system-message/<key>` using keys: `approach-proposer`, `approach-evaluator`, `problem-solver`, `expert-evaluator`, `researcher`, `orchestrator`.
  - `prompt_runner_background.html` is the background-mode variant and uses the same system-message loader keys.

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

### Core code snippets

**Image generation (server-side):**

```python
result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    n=n,
    **build_kwargs(data, for_generate=True),
)
```

**Multi-turn Responses call (server-side):**

```python
messages = [
    {"role": "developer", "content": [{"type": "input_text", "text": dev_message}]},
    {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
    {"role": "assistant", "content": [{"type": "output_text", "text": seed_reply}]},
    # ...more turns as needed...
]

response = client.responses.create(
    model="gpt-5.1",
    input=messages,
    text={"format": {"type": "text"}, "verbosity": "high"},
    reasoning={"effort": "high", "summary": None},
    tools=[{"type": "web_search", "user_location": {"type": "approximate"}, "search_context_size": "high"}],
    store=True,
)
```

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
