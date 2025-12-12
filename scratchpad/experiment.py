import os
import re
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")

client = OpenAI(api_key=api_key)

SCRATCHPAD_DIR = Path(__file__).resolve().parent
EXPERIMENT_HTML_PATH = SCRATCHPAD_DIR / "experiment.html"
MODEL_PATTERN = re.compile(r"^(gpt-5-pro|gpt-5\.\d+(-pro)?)$", re.IGNORECASE)
ALLOWED_REASONING = {"none", "low", "medium", "high", "xhigh"}
ALLOWED_VERBOSITY = {"low", "medium", "high"}
# Toggle this to False to return to the original behavior of omitting verbosity/effort on pro models.
ALLOW_PRO_REASONING_CONFIG = True


def _validate_choice(value: object, allowed: set, field: str, default: str) -> str:
    """Validate string choices for payload configuration."""

    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{field} must be one of: {', '.join(sorted(allowed))}.")

    normalized = value.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"{field} must be one of: {', '.join(sorted(allowed))}.")

    return normalized


def _normalize_model(value: object, default: str) -> str:
    """Ensure model names stay within the gpt-5.x / gpt-5.x-pro family."""

    if not isinstance(value, str) or not value.strip():
        return default

    model = value.strip()
    if not MODEL_PATTERN.match(model):
        raise ValueError("model must be gpt-5-pro or a gpt-5.x / gpt-5.x-pro model.")

    return model


def _is_pro_model(model: str) -> bool:
    """Return True if the provided model string refers to a pro variant."""

    return isinstance(model, str) and model.lower().endswith("-pro")


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


def create_prompt_response(
    messages: List[Dict[str, object]],
    *,
    model: str = "gpt-5.1",
    text_verbosity: str = "high",
    reasoning_effort: str = "high",
    background: bool = False,
) -> object:
    """Invoke Responses API with an ordered list of role/content messages."""

    if not messages:
        raise ValueError("At least one message is required.")

    is_pro_model = _is_pro_model(model)
    allow_pro_config = ALLOW_PRO_REASONING_CONFIG or not is_pro_model
    text_config: Dict[str, object] = {"format": {"type": "text"}}
    if allow_pro_config and text_verbosity:
        text_config["verbosity"] = text_verbosity

    reasoning_config: Dict[str, object] = {"summary": None}
    if allow_pro_config and reasoning_effort:
        reasoning_config["effort"] = reasoning_effort

    request_payload: Dict[str, object] = {
        "model": model or "gpt-5.1",
        "input": messages,
        "text": text_config,
        "reasoning": reasoning_config,
        "tools": [
            {
                "type": "web_search",
                "user_location": {"type": "approximate"},
                "search_context_size": "high",
            }
        ],
    }

    if background:
        request_payload["background"] = True
    else:
        request_payload["store"] = True

    return client.responses.create(**request_payload)


def create_background_prompt_response(
    messages: List[Dict[str, object]],
    *,
    model: str = "gpt-5.1-pro",
    text_verbosity: str = "high",
    reasoning_effort: str = "high",
):
    """Invoke Responses API in background mode with the supplied messages."""

    return create_prompt_response(
        messages,
        model=model,
        text_verbosity=text_verbosity,
        reasoning_effort=reasoning_effort,
        background=True,
    )


app = Flask(__name__)


@app.get("/")
def serve_frontend():
    if EXPERIMENT_HTML_PATH.exists():
        return send_file(EXPERIMENT_HTML_PATH)
    return ("experiment.html is missing. Generate it in the scratchpad directory.", 404)


@app.post("/api/prompt-run")
def handle_prompt_run():
    payload = request.get_json(silent=True) or {}

    try:
        messages = _normalize_messages(payload.get("messages"))
        model = _normalize_model(payload.get("model"), "gpt-5.1")
        is_pro_model = _is_pro_model(model)
        allow_pro_config = ALLOW_PRO_REASONING_CONFIG or not is_pro_model
        reasoning_effort = (
            _validate_choice(
                payload.get("reasoning_effort") or payload.get("effort"),
                ALLOWED_REASONING,
                "reasoning_effort",
                "high",
            )
            if allow_pro_config
            else None
        )
        text_verbosity = (
            _validate_choice(
                payload.get("text_verbosity") or payload.get("verbosity"),
                ALLOWED_VERBOSITY,
                "text_verbosity",
                "high",
            )
            if allow_pro_config
            else None
        )
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_prompt_response(
            messages,
            model=model,
            text_verbosity=text_verbosity or "high",
            reasoning_effort=reasoning_effort or "high",
            background=bool(payload.get("background")),
        )
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Prompt-based response creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_text = ""
    try:
        output_text = _extract_output_text(response)
    except Exception:  # pragma: no cover
        app.logger.exception("Failed to extract output_text content from response")

    return jsonify(ok=True, response=response.model_dump(), output_text=output_text)


@app.post("/api/prompt-run-background")
def handle_background_prompt_run():
    payload = request.get_json(silent=True) or {}

    try:
        messages = _normalize_messages(payload.get("messages"))
        model = _normalize_model(payload.get("model"), "gpt-5.1-pro")
        is_pro_model = _is_pro_model(model)
        allow_pro_config = ALLOW_PRO_REASONING_CONFIG or not is_pro_model
        reasoning_effort = (
            _validate_choice(
                payload.get("reasoning_effort") or payload.get("effort"),
                ALLOWED_REASONING,
                "reasoning_effort",
                "high",
            )
            if allow_pro_config
            else None
        )
        text_verbosity = (
            _validate_choice(
                payload.get("text_verbosity") or payload.get("verbosity"),
                ALLOWED_VERBOSITY,
                "text_verbosity",
                "high",
            )
            if allow_pro_config
            else None
        )
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_background_prompt_response(
            messages,
            model=model,
            text_verbosity=text_verbosity or "high",
            reasoning_effort=reasoning_effort or "high",
        )
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background prompt creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_text = ""
    try:
        output_text = _extract_output_text(response)
    except Exception:  # pragma: no cover
        app.logger.exception("Failed to extract output_text content from background response")

    return jsonify(
        ok=True,
        response_id=response.id,
        status=response.status,
        response=response.model_dump(),
        output_text=output_text,
    )


@app.get("/api/prompt-run-background/<response_id>")
def poll_background_prompt_run(response_id: str):
    try:
        response = client.responses.retrieve(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background prompt polling failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_text = ""
    try:
        output_text = _extract_output_text(response)
    except Exception:  # pragma: no cover
        app.logger.exception("Failed to extract output_text content from polled background response")

    payload = {
        "ok": True,
        "status": response.status,
        "response": response.model_dump(),
        "output_text": output_text,
    }
    payload["done"] = response.status in {"completed", "failed", "cancelled"}
    return jsonify(payload)


if __name__ == "__main__":
    host = os.getenv("TRY_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("TRY_SERVER_PORT", "2457"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
