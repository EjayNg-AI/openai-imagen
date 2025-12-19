import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")

client = OpenAI(api_key=api_key)

SCRATCHPAD_DIR = Path(__file__).resolve().parent
HTML_PATH = SCRATCHPAD_DIR / "json_output_playground.html"


def _require_str(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string.")
    trimmed = value.strip()
    if not trimmed:
        raise ValueError(f"{field} is required.")
    return trimmed


def _optional_str(value: object) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Expected a string.")
    trimmed = value.strip()
    return trimmed if trimmed else None


def _parse_schema(schema_value: object) -> Dict[str, Any]:
    if schema_value is None:
        raise ValueError("schema_json is required for json_schema format.")
    if isinstance(schema_value, dict):
        return schema_value
    if isinstance(schema_value, str):
        trimmed = schema_value.strip()
        if not trimmed:
            raise ValueError("schema_json is required for json_schema format.")
        try:
            parsed = json.loads(trimmed)
        except json.JSONDecodeError as exc:
            raise ValueError(f"schema_json is not valid JSON: {exc.msg}")
        if not isinstance(parsed, dict):
            raise ValueError("schema_json must be a JSON object.")
        return parsed
    raise ValueError("schema_json must be a JSON object or JSON string.")


def _extract_output_texts(response) -> List[str]:
    texts: List[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for block in getattr(item, "content", []) or []:
            if getattr(block, "type", None) != "output_text":
                continue
            text_blob = getattr(block, "text", "")
            if isinstance(text_blob, str) and text_blob.strip():
                texts.append(text_blob)
    return texts


def _parse_output_json(texts: List[str]) -> Tuple[List[Any], List[str]]:
    parsed: List[Any] = []
    errors: List[str] = []
    for index, text in enumerate(texts, start=1):
        try:
            parsed.append(json.loads(text))
        except json.JSONDecodeError as exc:
            errors.append(f"output_text[{index}] JSON error: {exc.msg}")
    return parsed, errors


def _build_text_config(payload: Dict[str, Any]) -> Dict[str, Any]:
    format_type = _optional_str(payload.get("format_type")) or "json_schema"
    verbosity = _optional_str(payload.get("verbosity")) or "medium"

    if format_type == "json_schema":
        schema_name = _optional_str(payload.get("schema_name")) or "json_schema_output"
        schema_json = _parse_schema(payload.get("schema_json"))
        return {
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": False,
                "schema": schema_json,
            },
            "verbosity": verbosity,
        }
    if format_type == "json_object":
        return {
            "format": {"type": "json_object"},
            "verbosity": verbosity,
        }
    raise ValueError("format_type must be json_schema or json_object.")


def _build_request_args(payload: Dict[str, Any]) -> Dict[str, Any]:
    developer_message = _require_str(payload.get("developer_message"), "developer_message")
    user_message = _require_str(payload.get("user_message"), "user_message")
    model = _require_str(payload.get("model"), "model")

    reasoning_effort = _optional_str(payload.get("reasoning_effort"))

    request_args: Dict[str, Any] = {
        "model": model,
        "instructions": developer_message,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_message}],
            }
        ],
        "text": _build_text_config(payload),
    }

    if reasoning_effort:
        request_args["reasoning"] = {"effort": reasoning_effort}
    return request_args


app = Flask(__name__)


@app.get("/")
def serve_frontend():
    if not HTML_PATH.exists():
        return "json_output_playground.html is missing.", 500
    return send_file(HTML_PATH)


@app.post("/api/json-output")
def run_json_output():
    payload = request.get_json(silent=True) or {}
    try:
        request_args = _build_request_args(payload)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = client.responses.create(**request_args)
    except Exception as exc:  # noqa: BLE001 - surface API failures to client
        app.logger.exception("OpenAI response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_texts = _extract_output_texts(response)
    parsed_outputs, parse_errors = _parse_output_json(output_texts)

    return jsonify(
        ok=True,
        response=response.model_dump(),
        output_texts=output_texts,
        parsed_outputs=parsed_outputs,
        parse_errors=parse_errors,
    )


if __name__ == "__main__":
    host = os.getenv("JSON_PLAYGROUND_HOST", "127.0.0.1")
    port = int(os.getenv("JSON_PLAYGROUND_PORT", "2261"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
