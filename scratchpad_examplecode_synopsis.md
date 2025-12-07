# `scratchpad/examplecode.py` OpenAI flow

- Loads `.env` via `dotenv`, pulls `OPENAI_API_KEY`, and refuses to start if missing; builds one `OpenAI` client reused across requests.

```python
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")
client = OpenAI(api_key=api_key)
```

- Declares a strict JSON schema to force five paragraph objects in the response.

```python
SCHEMA_DEFINITION = {
    "type": "object",
    "properties": {
        "paragraphs": {
            "type": "array",
            "description": "An array containing five paragraphs, each ranging from 150 to 200 words.",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "minLength": 800, "maxLength": 2000}
                },
                "required": ["text"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["paragraphs"],
    "additionalProperties": False,
}
```

## Request construction

- Inputs are validated up front: non-empty, each under 1000 words (else `ValueError`).

```python
def _validate_messages(developer_message: str, user_message: str) -> Tuple[str, str]:
    developer_message = developer_message.strip()
    user_message = user_message.strip()
    if not developer_message or not user_message:
        raise ValueError("Developer and user messages are required.")
    for label, message in (("Developer", developer_message), ("User", user_message)):
        if _word_count(message) > 1000:
            raise ValueError(f"{label} message exceeds the 1000-word limit.")
    return developer_message, user_message
```

- The OpenAI call itself uses the Responses API with the schema as a JSON output format.

```python
def create_story_response(developer_message: str, user_message: str):
    return client.responses.create(
        model="gpt-5",
        input=[
            {"role": "developer", "content": [{"type": "input_text", "text": developer_message}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_message}]},
        ],
        text={
            "format": {"type": "json_schema", "name": "five_paragraphs", "strict": True, "schema": SCHEMA_DEFINITION},
            "verbosity": "medium",
        },
        reasoning={"effort": "medium", "summary": "auto"},
        tools=[],
        store=True,
        include=["reasoning.encrypted_content", "web_search_call.action.sources"],
    )
```

## Response handling

- Paragraph extraction tolerates missing fields or malformed JSON and falls back to an empty list.

```python
def _extract_paragraphs(response) -> List[str]:
    paragraphs: List[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for block in getattr(item, "content", []) or []:
            if getattr(block, "type", None) != "output_text":
                continue
            text_blob = getattr(block, "text", "")
            if not isinstance(text_blob, str):
                continue
            try:
                payload = json.loads(text_blob)
            except json.JSONDecodeError:
                continue
            paragraphs_data = payload.get("paragraphs", [])
            if not isinstance(paragraphs_data, list):
                continue
            for entry in paragraphs_data:
                paragraph_text = entry.get("text") if isinstance(entry, dict) else None
                if isinstance(paragraph_text, str):
                    normalized = paragraph_text.strip()
                    if normalized:
                        paragraphs.append(normalized)
            if paragraphs:
                return paragraphs
    return paragraphs
```

- Behavior: walks only `message` → `output_text` blocks, parses JSON, collects trimmed `text` fields. If parsing fails at any step, the error is swallowed and the function returns an empty list.

## Flask endpoints

```python
@app.get("/")
def serve_frontend():
    if TRY_HTML_PATH.exists():
        return send_file(TRY_HTML_PATH)
    return ("try.html is missing. Generate it in the scratchpad directory.", 404)

@app.post("/api/responses")
def handle_response_request():
    payload = request.get_json(silent=True) or {}
    developer_message = payload.get("developer_message", "")
    user_message = payload.get("user_message", "")

    try:
        developer_message, user_message = _validate_messages(developer_message, user_message)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_story_response(developer_message, user_message)
    except Exception as exc:
        app.logger.exception("OpenAI response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    paragraphs: List[str] = []
    try:
        paragraphs = _extract_paragraphs(response)
    except Exception:
        app.logger.exception("Failed to extract paragraphs from response")

    return jsonify(ok=True, response=response.model_dump(), paragraphs=paragraphs)
```

- Flow: read JSON payload → validate → call OpenAI → on failure return `500` with logged stack → attempt extraction (logged on failure) → return success payload with raw `response.model_dump()` and possibly empty `paragraphs`.

## Prompt runner flow

- `create_prompt_response` calls the Responses API with both roles, trims inputs, enforces ≤1000 words, uses `gpt-5.1`, high verbosity/reasoning, and enables `web_search` (approximate location, high context). Responses are stored server-side.

```python
def create_prompt_response(developer_message: str, user_message: str):
    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message:
        raise ValueError("Developer message must be a non-empty string.")
    if not user_message:
        raise ValueError("User message must be a non-empty string.")

    for label, message in (("Developer", developer_message), ("User", user_message)):
        if _word_count(message) > 1000:
            raise ValueError(f"{label} message exceeds the 1000-word limit.")

    return client.responses.create(
        model="gpt-5.1",
        input=[
            {"role": "developer", "content": [{"type": "input_text", "text": developer_message}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_message}]},
        ],
        text={"format": {"type": "text"}, "verbosity": "high"},
        reasoning={"effort": "high", "summary": None},
        tools=[{"type": "web_search", "user_location": {"type": "approximate"}, "search_context_size": "high"}],
        store=True,
    )
```

- Backend endpoint `/api/prompt-run` validates string types + word counts, calls `create_prompt_response`, extracts assistant `output_text` blocks, and returns `{ok, response.model_dump(), output_text}`; API failures surface as `500`.

```python
@app.post("/api/prompt-run")
def handle_prompt_run():
    payload = request.get_json(silent=True) or {}
    developer_message = payload.get("developer_message", "")
    user_message = payload.get("user_message", "")

    if not isinstance(developer_message, str) or not isinstance(user_message, str):
        return jsonify(ok=False, error="developer_message and user_message must be strings."), 400

    try:
        developer_message = developer_message.strip()
        user_message = user_message.strip()
        if not developer_message or not user_message:
            raise ValueError("Developer and user messages are required.")
        if _word_count(developer_message) > 1000 or _word_count(user_message) > 1000:
            raise ValueError("Each message must be 1000 words or fewer.")
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_prompt_response(developer_message, user_message)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Prompt-based response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_text = ""
    try:
        output_text = _extract_output_text(response)
    except Exception:  # pragma: no cover
        app.logger.exception("Failed to extract output_text content from response")

    return jsonify(ok=True, response=response.model_dump(), output_text=output_text)
```

## Frontend prompt runner

- `scratchpad/prompt_runner.html` provides a two-textarea form and posts JSON to `/api/prompt-run`. It enforces non-empty fields and ≤1000 words client-side, disables controls while awaiting the response, and shows both the extracted assistant output and the raw payload.

```javascript
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  updateCount();

  const devTrimmed = developerField.value.trim();
  const userTrimmed = userField.value.trim();
  if (!devTrimmed || !userTrimmed) { showStatus("Developer and user messages are required.", true); return; }
  if (countWords(devTrimmed) > MAX_WORDS || countWords(userTrimmed) > MAX_WORDS) {
    showStatus("Please keep each message within 1000 words.", true);
    return;
  }

  const payload = { developer_message: devTrimmed, user_message: userTrimmed };
  setDisabled(true);
  showStatus("Sending request…");

  try {
    const response = await fetch("/api/prompt-run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const rawText = await response.text();
    let parsed;
    try { parsed = JSON.parse(rawText); } catch { parsed = rawText; }

    const ok = response.ok && parsed && parsed.ok !== false;
    if (!ok) {
      const err = (parsed && parsed.error) || (typeof parsed === "string" ? parsed : null) ||
        `Request failed with status ${response.status}`;
      showStatus(err, true);
      outputBox.value = "";
    } else {
      showStatus("Received response from OpenAI.");
      const text = (parsed && parsed.output_text) ||
        (parsed && parsed.response && parsed.response.output) || "";
      outputBox.value = typeof text === "string" ? text : JSON.stringify(text, null, 2) || "";
    }

    rawPayload.textContent = typeof parsed === "string"
      ? parsed
      : JSON.stringify(parsed, null, 2) || "(empty response)";
  } catch (error) {
    console.error("Network error", error);
    showStatus(`Network error: ${error.message}`, true);
    outputBox.value = "";
    rawPayload.textContent = "(no response received)";
  } finally {
    setDisabled(false);
  }
});
```

## Error detection and fallbacks

- Startup guard: missing API key raises `RuntimeError`.
- Input guard: empty or >1000-word messages short-circuit with `400`.
- API guard: any `responses.create` exception results in `500` plus the error message, logged with traceback.
- Parsing guard: extraction ignores malformed/missing data and logs on unexpected exceptions, returning an empty list so callers still receive the raw model dump.
