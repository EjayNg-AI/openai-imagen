import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")

client = OpenAI(api_key=api_key)

SCRATCHPAD_DIR = Path(__file__).resolve().parent


def _validate_paragraph_count(value: object, *, default: int = 5) -> int:
    """Coerce and clamp the paragraph count within safe bounds."""

    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError("paragraph_count must be an integer.")
    if not 1 <= parsed <= 10:
        raise ValueError("paragraph_count must be between 1 and 10.")
    return parsed


def _build_paragraph_schema(count: int) -> Dict[str, object]:
    """Create a JSON schema that requires exactly `count` paragraphs."""

    return {
        "type": "object",
        "properties": {
            "paragraphs": {
                "type": "array",
                "description": f"An array containing {count} paragraphs, each ranging from 250 to 350 words.",
                "minItems": count,
                "maxItems": count,
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The content of the paragraph (plain text).",
                            "minLength": 1250,
                            "maxLength": 2450,
                        }
                    },
                    "required": ["text"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["paragraphs"],
        "additionalProperties": False,
    }


def create_story_response(developer_message: str, user_message: str, *, paragraph_count: int = 5):
    """Invoke the Responses API using the supplied developer and user messages."""

    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message or not user_message:
        raise ValueError("Both developer_message and user_message must be non-empty strings.")

    paragraph_count = _validate_paragraph_count(paragraph_count)

    return client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": developer_message,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_message,
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": f"paragraphs_{paragraph_count}",
                "strict": True,
                "schema": _build_paragraph_schema(paragraph_count),
            },
            "verbosity": "medium",
        },
        reasoning={
            "effort": "medium",
            "summary": "auto",
        },
        tools=[],
        store=True,
        include=[
            "reasoning.encrypted_content",
            "web_search_call.action.sources",
        ],
    )


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


def _validate_messages(developer_message: str, user_message: str) -> Tuple[str, str]:
    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message or not user_message:
        raise ValueError("Developer and user messages are required.")

    return developer_message, user_message


app = Flask(__name__)

TRY_HTML_PATH = SCRATCHPAD_DIR / "try.html"
if not TRY_HTML_PATH.exists():
    raise SystemExit("try.html is missing. Generate it in the scratchpad directory.")


@app.get("/")
def serve_frontend():
    return send_file(TRY_HTML_PATH)


@app.post("/api/responses")
def handle_response_request():
    payload = request.get_json(silent=True) or {}
    developer_message = payload.get("developer_message", "")
    user_message = payload.get("user_message", "")
    paragraph_count_raw = payload.get("paragraph_count", 5)

    try:
        developer_message, user_message = _validate_messages(developer_message, user_message)
        paragraph_count = _validate_paragraph_count(paragraph_count_raw)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_story_response(
            developer_message,
            user_message,
            paragraph_count=paragraph_count,
        )
    except Exception as exc:  # noqa: BLE001 - surface API failures to client
        app.logger.exception("OpenAI response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    paragraphs: List[str] = []
    try:
        paragraphs = _extract_paragraphs(response)
    except Exception:  # pragma: no cover - defensive logging
        app.logger.exception("Failed to extract paragraphs from response")

    return jsonify(ok=True, response=response.model_dump(), paragraphs=paragraphs)


if __name__ == "__main__":
    host = os.getenv("TRY_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("TRY_SERVER_PORT", "2357"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
