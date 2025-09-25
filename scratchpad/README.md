# Scratchpad Investigation Notes

## Context
- **Script**: `scratchpad/examplecode.py`
- **Goals**:
  - Produce and inspect OpenAI `Response` objects using credentials from `.env`
  - Host a local Flask API (`/api/responses`) that forwards developer/user instructions to `OpenAI.responses.create`
  - Serve a companion dark-themed frontend (`scratchpad/try.html`) on the root path
- **Artifacts**:
  - Structured dump saved to `scratchpad/last_response.json`
  - Exposed paragraph list in every API response (`"paragraphs": [...]`)

## Execution Timeline
1. **Initial run (sandboxed)**
   - Command: `python scratchpad/examplecode.py`
   - Result: `openai.APIConnectionError` caused by `httpx.ConnectError` (`Temporary failure in name resolution`).
   - Cause: Network-denied sandbox prevented reaching the OpenAI API endpoint.
2. **Escalated rerun**
   - Command rerun with `with_escalated_permissions=true`.
   - Result: Successful completion; `Response` object instantiated and stored in-memory.
3. **Interactive inspections**
   - Multiple short Python snippets invoked with escalation to introspect the response, capture usage metrics, and finally persist the full `model_dump()` JSON to disk.
4. **Flask wiring**
   - Converted `examplecode.py` into a Flask app that exposes `/` (serving `try.html`) and `/api/responses` (calling the Responses API and extracting paragraphs).
   - Added defensive validation (1000-word cap per message) and parsing helpers to ensure the frontend always receives a clean paragraph list when the model honours the schema.

## Failure Modes & Resolutions
- **Network resolution failure**
  - *Symptom*: `Temporary failure in name resolution` inside the HTTP client stack.
  - *Resolution*: Request elevated execution (network-enabled) and rerun. Subsequent API calls succeeded.
- **Timeouts during long inspections**
  - *Symptom*: `command timed out` when attempting to print large sections of the response directly in the REPL.
  - *Resolution*: Limit per-call interrogation and offload detailed inspection to a saved JSON artifact (`scratchpad/last_response.json`).
- **Attribute access error**
  - *Symptom*: Attempting `resp.usage.prompt_tokens` raised `AttributeError` because only `input_tokens`, `output_tokens`, and `total_tokens` fields are exposed.
  - *Resolution*: Inspected `resp.usage.model_dump()` to list available keys and relied on those explicitly provided.

## Response Object Highlights
- **Type**: `openai.types.responses.response.Response`
- **Identifiers**:
  - `id`: e.g., `resp_68d4c233ad5c819db3d7b180cee6dcad0dd82b36797dc30c`
  - `model`: `gpt-5-2025-08-07`
  - `created_at`: `2025-09-25T04:16:51Z`
- **Output entries**:
  1. `type="reasoning"` — contains six `summary_text` items outlining internal planning (full chain-of-thought kept in `encrypted_content`).
  2. `type="message"` — role `assistant`, single `output_text` field containing the JSON payload required by the schema.
- **Final content**: JSON with `paragraphs` array; each element holds a 150–200 word short story (two focused on office workers). Word counts verified: `[164, 169, 168, 171, 170]`.
- **Paragraph extraction**: `_extract_paragraphs` walks the assistant message → `output_text` payload, decodes the JSON, and surfaces a trimmed list of strings. The frontend displays these in a high-contrast textarea for readability.
- **Usage metrics**:
  - `input_tokens`: 105 (no cached tokens)
  - `output_tokens`: 5,311 with `reasoning_tokens`: 4,224
  - `total_tokens`: 5,416
- **Metadata**: Empty object; `billing.payer` reports `openai`; `store` flag true.

## Persisted Artifact
- Path: `scratchpad/last_response.json`
- Contents: Full `model_dump()` from the successful response, suitable for downstream inspection or regression comparisons.

## Flask playground
- Start with `python scratchpad/examplecode.py` (defaults to `http://127.0.0.1:2357`).
- `GET /` → serves `scratchpad/try.html` (now dark-themed for comfortable viewing).
- `POST /api/responses` → expects `{ "developer_message": "...", "user_message": "..." }`. It validates word counts, proxies to `OpenAI.responses.create`, and answers with:
  ```json
  {
    "ok": true,
    "response": { ... full model_dump ... },
    "paragraphs": ["Paragraph 1 text", "Paragraph 2 text", ...]
  }
  ```
- Errors bubble up as `{"ok": false, "error": "..."}` with HTTP `400/500` codes for the frontend to report.

## Frontend (`try.html`)
- Provides two 1000-word textareas (developer/user roles) with live word counts.
- Uses the new dark palette shared with the main playground; form controls and result panels are tuned for high contrast in low-light environments.
- Displays the raw backend payload in a code panel and the extracted paragraphs in a dedicated textbox so you can copy-review the stories without manual JSON parsing.

## Suggested Follow-ups
- Build lightweight parser utilities that consume `scratchpad/last_response.json` to experiment with downstream formatting or validation logic.
- When re-running `examplecode.py`, ensure network-enabled execution up front to avoid resolution errors.
- Extend the Flask endpoint to accept custom schemas or toggle `store`/`reasoning` options for broader experimentation.
