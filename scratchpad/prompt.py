import os
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
CONSOLIDATED_SYSTEM_MESSAGES_PATH = SCRATCHPAD_DIR / "system_messages_consolidated.md"
SYSTEM_MESSAGE_HEADINGS = {
    "approach-proposer": "APPROACH_PROPOSER SYSTEM MESSAGE (TO PROPOSE POSSIBLE SOLUTION "
    "APPROACHES FOR A GIVEN PROBLEM)",
    "approach-evaluator": "APPROACH_EVALUATOR SYSTEM MESSAGE (TO EVALUATE POSSIBLE SOLUTION "
    "APPROACHES SUGGESTED BY A PROBLEM_SOLVER)",
    "problem-solver": "PROBLEM_SOLVER SYSTEM MESSAGE (TO ATTEMPT A SOLUTION TO A GIVEN PROBLEM)",
    "expert-evaluator": "EXPERT_SOLUTION_EVALUATOR SYSTEM MESSAGE (TO EVALUATE THE MOST RECENT "
    "SOLUTION ATTEMPT BY A PROBLEM_SOLVER)",
    "researcher": "RESEARCHER SYSTEM MESSAGE (TO PROVIDE EXTERNAL RESEARCH INPUT)",
    "orchestrator": "ORCHESTRATOR SYSTEM MESSAGE (AUTOMATION-FRIENDLY + FINAL POLISHER)",
    "synthesizer-planner": "APPROACH_PROPOSER SYSTEM MESSAGE (TO PROPOSE POSSIBLE SOLUTION "
    "APPROACHES FOR A GIVEN PROBLEM)",
    "discriminator-approach-evaluator": "APPROACH_EVALUATOR SYSTEM MESSAGE (TO EVALUATE POSSIBLE "
    "SOLUTION APPROACHES SUGGESTED BY A PROBLEM_SOLVER)",
    "synthesizer-solver": "PROBLEM_SOLVER SYSTEM MESSAGE (TO ATTEMPT A SOLUTION TO A GIVEN PROBLEM)",
    "discriminator-solution-evaluator": "EXPERT_SOLUTION_EVALUATOR SYSTEM MESSAGE (TO EVALUATE THE "
    "MOST RECENT SOLUTION ATTEMPT BY A PROBLEM_SOLVER)",
}


def _clean_system_message(lines: List[str]) -> str:
    content = list(lines)
    while content and not content[0].strip():
        content.pop(0)
    while content and not content[-1].strip():
        content.pop()
    if content and content[-1].strip() == "---":
        content.pop()
        while content and not content[-1].strip():
            content.pop()
    return "\n".join(content)


def _parse_consolidated_system_messages() -> Dict[str, str]:
    if not CONSOLIDATED_SYSTEM_MESSAGES_PATH.exists():
        raise FileNotFoundError(f"{CONSOLIDATED_SYSTEM_MESSAGES_PATH.name} is missing")

    text = CONSOLIDATED_SYSTEM_MESSAGES_PATH.read_text(encoding="utf-8")
    sections: Dict[str, str] = {}
    current_heading = None
    buffer: List[str] = []

    for line in text.splitlines():
        if line.startswith("# "):
            if current_heading is not None:
                sections[current_heading] = _clean_system_message(buffer)
            current_heading = line[2:].strip()
            buffer = []
            continue
        if current_heading is None:
            continue
        buffer.append(line)

    if current_heading is not None:
        sections[current_heading] = _clean_system_message(buffer)

    return sections


def _read_system_message(key: str) -> str:
    heading = SYSTEM_MESSAGE_HEADINGS.get(key)
    if not heading:
        raise KeyError(f"Unknown system message key: {key}")

    sections = _parse_consolidated_system_messages()
    content = sections.get(heading)
    if content is None:
        raise KeyError(f"System message heading not found: {heading}")
    return content


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

    text_config: Dict[str, object] = {"format": {"type": "text"}}
    if text_verbosity:
        text_config["verbosity"] = text_verbosity

    reasoning_config: Dict[str, object] = {"summary": None}
    if reasoning_effort:
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
    model: str = "gpt-5-pro",
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

PROMPT_HTML_PATH = Path(__file__).resolve().parent / "prompt_runner.html"
PROMPT_BACKGROUND_HTML_PATH = Path(__file__).resolve().parent / "prompt_runner_background.html"


@app.get("/")
def serve_frontend():
    if PROMPT_HTML_PATH.exists():
        return send_file(PROMPT_HTML_PATH)
    return ("prompt_runner.html is missing. Generate it in the scratchpad directory.", 404)


@app.get("/prompt-runner")
def serve_prompt_frontend():
    if PROMPT_HTML_PATH.exists():
        return send_file(PROMPT_HTML_PATH)
    return (
        "prompt_runner.html is missing. Generate it in the scratchpad directory.",
        404,
    )


@app.get("/prompt-runner-background")
def serve_background_prompt_frontend():
    if PROMPT_BACKGROUND_HTML_PATH.exists():
        return send_file(PROMPT_BACKGROUND_HTML_PATH)
    return (
        "prompt_runner_background.html is missing. Generate it in the scratchpad directory.",
        404,
    )


@app.get("/api/system-message/<key>")
def handle_system_message(key: str):
    try:
        content = _read_system_message(key)
    except KeyError:
        return jsonify(ok=False, error="Unknown system message key."), 404
    except FileNotFoundError as exc:
        app.logger.error("System message file missing: %s", exc)
        return jsonify(ok=False, error=str(exc)), 404
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Failed to read system message %s", key)
        return jsonify(ok=False, error="Failed to read system message file."), 500
    return jsonify(ok=True, key=key, content=content)


@app.post("/api/prompt-run")
def handle_prompt_run():
    payload = request.get_json(silent=True) or {}

    messages: List[Dict[str, object]] = []

    try:
        messages = _normalize_messages(payload.get("messages"))
        model = (
            payload.get("model").strip()
            if isinstance(payload.get("model"), str) and payload.get("model").strip()
            else "gpt-5.1"
        )
        reasoning_effort = _validate_choice(
            payload.get("reasoning_effort") or payload.get("effort"),
            {"none", "low", "medium", "high", "xhigh"},
            "reasoning_effort",
            "high",
        )
        text_verbosity = _validate_choice(
            payload.get("text_verbosity") or payload.get("verbosity"),
            {"low", "medium", "high"},
            "text_verbosity",
            "high",
        )
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    try:
        response = create_prompt_response(
            messages,
            model=model,
            text_verbosity=text_verbosity or "high",
            reasoning_effort=reasoning_effort or "high",
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
        model = (
            payload.get("model").strip()
            if isinstance(payload.get("model"), str) and payload.get("model").strip()
            else "gpt-5-pro"
        )

        reasoning_effort = _validate_choice(
            payload.get("reasoning_effort") or payload.get("effort"),
            {"none", "low", "medium", "high", "xhigh"},
            "reasoning_effort",
            "high",
        )
        text_verbosity = _validate_choice(
            payload.get("text_verbosity") or payload.get("verbosity"),
            {"low", "medium", "high"},
            "text_verbosity",
            "high",
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


@app.post("/api/prompt-run-background/<response_id>/cancel")
def cancel_background_prompt_run(response_id: str):
    if not response_id:
        return jsonify(ok=False, error="response_id is required."), 400

    try:
        response = client.responses.cancel(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background prompt cancellation failed")
        return jsonify(ok=False, error=str(exc)), 500

    payload = {
        "ok": True,
        "status": response.status,
        "response": response.model_dump(),
    }
    payload["done"] = response.status in {"completed", "failed", "cancelled"}
    return jsonify(payload)


if __name__ == "__main__":
    host = os.getenv("TRY_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("TRY_SERVER_PORT", "2657"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
