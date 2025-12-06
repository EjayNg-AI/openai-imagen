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


SCHEMA_DEFINITION: Dict[str, object] = {
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
                    "text": {
                        "type": "string",
                        "description": "The content of the paragraph (plain text).",
                        "minLength": 800,
                        "maxLength": 2000,
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


def create_story_response(developer_message: str, user_message: str):
    """Invoke the Responses API using the supplied developer and user messages."""

    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message or not user_message:
        raise ValueError("Both developer_message and user_message must be non-empty strings.")

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
                "name": "five_paragraphs",
                "strict": True,
                "schema": SCHEMA_DEFINITION,
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


def create_prompt_response(developer_message: str, user_message: str):
    """Invoke Responses API with explicit developer + user roles and no schema."""

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
        text={"format": {"type": "text"}, "verbosity": "high"},
        reasoning={"effort": "high", "summary": None},
        tools=[
            {
                "type": "web_search",
                "user_location": {"type": "approximate"},
                "search_context_size": "high",
            }
        ],
        store=True,
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


def _extract_output_text(response) -> str:
    """Pull the assistant's output_text blocks and join them for display."""

    chunks: List[str] = []

    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for block in getattr(item, "content", []) or []:
            if getattr(block, "type", None) != "output_text":
                continue
            text_blob = getattr(block, "text", "")
            if isinstance(text_blob, str):
                normalized = text_blob.strip()
                if normalized:
                    chunks.append(normalized)

    return "\n\n".join(chunks).strip()


def _word_count(text: str) -> int:
    return len([token for token in text.strip().split() if token])


def _validate_messages(developer_message: str, user_message: str) -> Tuple[str, str]:
    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message or not user_message:
        raise ValueError("Developer and user messages are required.")

    for label, message in (("Developer", developer_message), ("User", user_message)):
        if _word_count(message) > 1000:
            raise ValueError(f"{label} message exceeds the 1000-word limit.")

    return developer_message, user_message


app = Flask(__name__)

TRY_HTML_PATH = Path(__file__).resolve().parent / "try.html"
PROMPT_HTML_PATH = Path(__file__).resolve().parent / "prompt_runner.html"


@app.get("/")
def serve_frontend():
    if TRY_HTML_PATH.exists():
        return send_file(TRY_HTML_PATH)
    return ("try.html is missing. Generate it in the scratchpad directory.", 404)


@app.get("/prompt-runner")
def serve_prompt_frontend():
    if PROMPT_HTML_PATH.exists():
        return send_file(PROMPT_HTML_PATH)
    return (
        "prompt_runner.html is missing. Generate it in the scratchpad directory.",
        404,
    )


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
    except Exception as exc:  # noqa: BLE001 - surface API failures to client
        app.logger.exception("OpenAI response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    paragraphs: List[str] = []
    try:
        paragraphs = _extract_paragraphs(response)
    except Exception:  # pragma: no cover - defensive logging
        app.logger.exception("Failed to extract paragraphs from response")

    return jsonify(ok=True, response=response.model_dump(), paragraphs=paragraphs)


@app.post("/api/prompt-run")
def handle_prompt_run():
    payload = request.get_json(silent=True) or {}
    developer_message = payload.get("developer_message", "")
    user_message = payload.get("user_message", "")

    if not isinstance(developer_message, str) or not isinstance(user_message, str):
        return (
            jsonify(ok=False, error="developer_message and user_message must be strings."),
            400,
        )

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


if __name__ == "__main__":
    host = os.getenv("TRY_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("TRY_SERVER_PORT", "2357"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
