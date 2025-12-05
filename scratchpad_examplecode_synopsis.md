# `scratchpad/examplecode.py` OpenAI flow

- Loads `.env` via `dotenv`, pulls `OPENAI_API_KEY`, and refuses to start if missing; constructs a single `OpenAI` client reused for all calls.
- Declares a strict JSON schema (`SCHEMA_DEFINITION`) requiring five paragraph objects with 150–200 words each; used to force structured output.

## Request construction

- `_validate_messages` trims inputs, ensures both are present, and caps each at 1000 words (raises `ValueError` on failure).
- `create_story_response(developer_message, user_message)` builds a `responses.create` call:
  - Model `gpt-5`; developer and user inputs are passed as `input_text` blocks.
  - `text.format` wraps the schema with `strict=True` under the name `five_paragraphs`; verbosity set to `medium`.
  - `reasoning` requested (`effort="medium"`, `summary="auto"`); `tools` empty; `store=True`; `include` asks for encrypted reasoning content and web-search source metadata.
  - Any exception during this call is treated as a server error by the API route.

## Response handling

- `_extract_paragraphs(response)` walks `response.output` items of type `message`, then `content` blocks of type `output_text`.
- Each text blob is parsed as JSON; if it matches the schema shape, paragraph `text` fields are stripped and collected.
- Returns the first non-empty list found; otherwise returns an empty list if parsing fails or nothing matches (guards against missing fields, wrong types, or JSON decode errors).

## Flask endpoints

- `GET /`: serves `scratchpad/try.html` if present; otherwise returns a 404 message prompting to generate it.
- `POST /api/responses` flow:
  - Reads `developer_message` and `user_message` from JSON payload (defaulting to empty strings).
  - Validates inputs; on `ValueError`, responds `400` with `ok=False` and the message.
  - Invokes `create_story_response`; any exception triggers a logged stack trace and a `500` with `ok=False` plus the error string.
  - Attempts to extract paragraphs; extraction errors are logged but do not fail the request—`paragraphs` simply stays empty.
  - Successful path returns `ok=True`, the full `response.model_dump()`, and the extracted `paragraphs` (possibly empty as a fallback).

## Error detection and fallbacks

- Startup guard: raises `RuntimeError` if `OPENAI_API_KEY` is missing.
- Input guard: word-count and emptiness checks return `400` before hitting the API.
- API guard: any `responses.create` failure yields a `500` with the exception message; no retries are implemented.
- Parsing guard: resilient JSON extraction with type checks and `JSONDecodeError` handling; failures degrade gracefully to an empty `paragraphs` list while logging the stack trace for debugging.
