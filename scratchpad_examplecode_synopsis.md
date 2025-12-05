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

## Error detection and fallbacks

- Startup guard: missing API key raises `RuntimeError`.
- Input guard: empty or >1000-word messages short-circuit with `400`.
- API guard: any `responses.create` exception results in `500` plus the error message, logged with traceback.
- Parsing guard: extraction ignores malformed/missing data and logs on unexpected exceptions, returning an empty list so callers still receive the raw model dump.
