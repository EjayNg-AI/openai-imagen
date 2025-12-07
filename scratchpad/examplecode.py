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
            "description": "An array containing five paragraphs, each ranging from 250 to 350 words.",
            "minItems": 5,
            "maxItems": 5,
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


def create_prompt_response(
    messages: List[Dict[str, object]],
) -> object:
    """Invoke Responses API with an ordered list of role/content messages."""

    if not messages:
        raise ValueError("At least one message is required.")

    return client.responses.create(
        model="gpt-5.1",
        input=messages,
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


def _validate_messages(developer_message: str, user_message: str) -> Tuple[str, str]:
    developer_message = developer_message.strip()
    user_message = user_message.strip()

    if not developer_message or not user_message:
        raise ValueError("Developer and user messages are required.")

    return developer_message, user_message


def _build_two_message_input(developer_message: str, user_message: str) -> List[Dict[str, object]]:
    developer_message, user_message = _validate_messages(developer_message, user_message)

    return [
        {
            "role": "developer",
            "content": [{"type": "input_text", "text": developer_message}],
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": user_message}],
        },
    ]


def _normalize_messages(messages: object) -> List[Dict[str, object]]:
    """Validate and normalize a list of conversation messages."""

    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a non-empty list.")

    allowed_roles = {"developer", "user", "assistant"}
    normalized: List[Dict[str, object]] = []

    for idx, item in enumerate(messages):
        if not isinstance(item, dict):
            raise ValueError(f"Message #{idx + 1} must be an object.")

        role_raw = item.get("role")
        role = role_raw.lower().strip() if isinstance(role_raw, str) else None
        if role not in allowed_roles:
            raise ValueError(
                f"Message #{idx + 1} has invalid role. Expected one of {sorted(allowed_roles)}."
            )

        content = item.get("content")
        if not isinstance(content, list) or not content:
            raise ValueError(f"Message #{idx + 1} must include a non-empty content array.")

        normalized_blocks: List[Dict[str, str]] = []
        default_type = "output_text" if role == "assistant" else "input_text"

        for block in content:
            if not isinstance(block, dict):
                continue
            text = block.get("text")
            if not isinstance(text, str):
                continue
            text = text.strip()
            if not text:
                continue

            block_type = block.get("type") if isinstance(block.get("type"), str) else default_type
            if role != "assistant":
                block_type = "input_text"
            elif block_type not in {"output_text", "input_text"}:
                block_type = default_type

            normalized_blocks.append({"type": block_type, "text": text})

        if not normalized_blocks:
            raise ValueError(f"Message #{idx + 1} is missing text content.")

        normalized.append({"role": role, "content": normalized_blocks})

    return normalized


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

    messages: List[Dict[str, object]] = []

    try:
        if "messages" in payload:
            messages = _normalize_messages(payload.get("messages"))
        else:
            developer_message = payload.get("developer_message", "")
            user_message = payload.get("user_message", "")
            if not isinstance(developer_message, str) or not isinstance(user_message, str):
                raise ValueError("developer_message and user_message must be strings.")
            messages = _build_two_message_input(developer_message, user_message)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_prompt_response(messages)
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
