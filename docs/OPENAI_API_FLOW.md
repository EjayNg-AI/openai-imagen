# OpenAI API Flows in This Repository

This document explains how the Python backends call the OpenAI API, which models are used, the validation and fallback logic, how errors are surfaced, and how the HTML frontends interact with the Flask endpoints. You can use it as a template for your own implementations.

## Prerequisites

- Python dependencies: `Flask`, `openai`, `Pillow`, `python-dotenv` (see `requirements.txt`).
- Environment: `.env` file with `OPENAI_API_KEY`. The app exits if this key is missing.
- Local run: `python app.py` (main image playground) or `python scratchpad/examplecode.py` (Responses API demo).

## Client Initialization (common)

```python
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY missing in environment")

client = OpenAI(api_key=api_key)
```

Failing fast on a missing key prevents later, harder-to-diagnose API errors.

## Image Generation (`/generate`) – model: `gpt-image-1`

Endpoint: `POST /generate` (`app.py`)

Key steps:
1. **Validate input**
   - Require `prompt`.
   - Parse `n` as int and enforce `1 <= n <= 8`.
   - If `background=transparent`, only allow `png`/`webp` output formats.
2. **Build OpenAI arguments**
   - Optional args forwarded when present: `size`, `quality`, `background`, `output_format`, `output_compression`, `moderation`.
3. **Call API**

   ```python
   result = client.images.generate(
       model="gpt-image-1",
       prompt=prompt,
       n=n,
       **build_kwargs(data, for_generate=True),
   )
   ```

4. **Return + persist**
   - For each returned item, decode `b64_json`, write the bytes to `saved_images/`, and send both a `data_uri` (for instant preview) and a saved URL.
5. **Errors**
   - Validation issues → `400 {ok:false, error:"..."}`.
   - API or unexpected issues → log stack trace, return `500 {ok:false, error:str(e)}`.

## Image Edit / Combine / Out-paint (`/edit`) – model: `gpt-image-1`

Endpoint: `POST /edit` (`app.py`)

Accepted inputs:
- `prompt` (required).
- Up to 10 reference images (`image1`…`image10`); each must be RGB/RGBA, ≤25 MB, and all must share the same dimensions.
- Optional `mask` PNG; must match ref dimensions. If no mask is provided and only one ref image is supplied with a filename starting `outpaint`, the server auto-derives a mask from transparent pixels.
- Optional args forwarded: `size`, `quality`, `background`, `n` (validated to 1–8 if provided).

API call:

```python
result = client.images.edit(
    model="gpt-image-1",
    prompt=prompt,
    image=images,  # list of io.BytesIO buffers, each with .name set
    **kwargs,      # may include mask, size, quality, background, n
)

returned_fmt = images[0].name.rsplit(".", 1)[-1]
b64 = result.data[0].b64_json
img_bytes = base64.b64decode(b64)
url = save_bytes(img_bytes, returned_fmt)
return jsonify(ok=True, data_uri=b64_to_datauri(b64, returned_fmt), url=url)
```

Errors:
- Validation failures (missing prompt, bad `n`, mismatched sizes, non-PNG mask, etc.) → `400`.
- API/other errors → logged, `500 {ok:false, error:str(e)}`.

## Validation & Fallback Mechanics

- **Transparency guard:** `background=transparent` only allowed with `png`/`webp` formats (prevents API rejection).
- **Image limits:** size ≤25 MB, mode RGB/RGBA, identical dimensions across refs; ensures server-side and OpenAI-side acceptance.
- **Mask handling:** If mask lacks an alpha channel, it is auto-converted to RGBA. Out-paint auto-mask is generated when a single image named `outpaint.*` is provided.
- **Safe `n` handling:** Parsed via `parse_int`; invalid values fallback to defaults or return 400.
- **Logging:** Exceptions are logged with stack traces to `app.log` to aid debugging.

## Persistence

- All returned images are decoded and stored under `saved_images/` with timestamp + UUID filenames.
- Files are served at `/saved/<filename>` via `send_from_directory`.
- Frontend receives both in-memory previews (`data_uri`) and persisted URLs.

## Frontend Interaction (Image Playground)

Frontend: `templates/index.html` (vanilla JS)
- Uses `fetch` with `FormData` to hit `/generate` and `/edit`.
- Client-side validation mirrors backend checks (prompt required, transparent background only for PNG/WEBP, mask readiness, at least one ref image).
- UI affordances: disabled buttons + spinners during requests; toast notifications for errors; auto-clears prior results before new calls.
- Mask/out-paint UI: draws mask on a canvas, exports as PNG Blob when submitted; optional “Expand” adds transparent borders for out-painting and auto-masks the original region.

Error handling on the client:
- `post()` helper inspects HTTP status and content type; non-JSON or network errors are coerced into `{ok:false, error:"..."}`.
- Unexpected success payloads (e.g., empty images) trigger user-facing toasts instead of silent failure.

## Responses API Playground (`scratchpad/examplecode.py`) – model: `gpt-5`

Purpose: demonstrate `OpenAI.responses.create` with schema enforcement and post-processing.

Flow:
1. Validate developer/user messages (non-empty, ≤1000 words).
2. Call `client.responses.create` with:
   - `model="gpt-5"`
   - `input` messages (developer/user, `input_text`)
   - `text.format` using `json_schema` (strict) for five paragraphs
   - `reasoning` opts, `tools=[]`, `store=True`, selective `include`
3. Extract paragraph strings from the structured response; failures to parse are logged but do not block returning the raw payload.
4. Return JSON: `{ok, response: response.model_dump(), paragraphs}`; 400 on validation errors; 500 on API errors.

Frontend: `scratchpad/try.html`
- Posts JSON to `/api/responses`.
- Enforces word limits client-side; shows inline status/errors; pretty-prints the raw backend response and displays extracted paragraphs in a textarea.

## Reuse Checklist

- Load `OPENAI_API_KEY` early and abort if missing.
- Centralize allowed kwargs to avoid sending unsupported params.
- Validate inputs (ranges, formats, dimensions) before calling the API.
- Wrap API calls in `try/except`; log exceptions and return structured JSON with appropriate HTTP status codes.
- Return both previews and persisted URLs when dealing with binary outputs.
- Mirror server validations client-side for faster feedback but keep server-side checks authoritative.
