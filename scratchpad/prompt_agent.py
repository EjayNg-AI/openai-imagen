import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

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
ORCHESTRATOR_SCHEMA_HEADING = "SCHEMA FOR ORCHESTRA API CALL"
DEFAULT_STATE_FILENAME = "agentic_workflow_state.json"
STATE_PATH = SCRATCHPAD_DIR / DEFAULT_STATE_FILENAME
STATE_FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,120}$")
SNAPSHOT_DIR = SCRATCHPAD_DIR / "saved_snapshots"
SNAPSHOT_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,160}$")
SNAPSHOT_FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,320}$")
_ORCHESTRATOR_SCHEMA_CACHE: Optional[Dict[str, object]] = None


def _normalize_state_filename(filename: Optional[str]) -> str:
    if not filename:
        return DEFAULT_STATE_FILENAME
    cleaned = filename.strip()
    if not cleaned:
        return DEFAULT_STATE_FILENAME
    if not STATE_FILENAME_RE.match(cleaned):
        raise ValueError(
            "Invalid state filename. Use letters, numbers, dots, dashes, or underscores only."
        )
    if not cleaned.endswith(".json"):
        cleaned = f"{cleaned}.json"
    return cleaned


def _resolve_state_path(filename: Optional[str]) -> Path:
    return SCRATCHPAD_DIR / _normalize_state_filename(filename)


def _ensure_snapshot_dir() -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _resolve_snapshot_path(filename: Optional[str], label: str) -> Path:
    if not isinstance(label, str):
        raise ValueError("snapshot label must be a string.")
    cleaned_label = label.strip()
    if not cleaned_label:
        raise ValueError("snapshot label is required.")
    if not SNAPSHOT_LABEL_RE.match(cleaned_label):
        raise ValueError(
            "Invalid snapshot label. Use letters, numbers, dots, dashes, or underscores only."
        )

    base_name = _normalize_state_filename(filename)
    base_stem = Path(base_name).stem
    snapshot_filename = f"{base_stem}_{cleaned_label}.json"
    if not SNAPSHOT_FILENAME_RE.match(snapshot_filename):
        raise ValueError("Invalid snapshot filename.")
    return SNAPSHOT_DIR / snapshot_filename


def _resolve_snapshot_name(name: str) -> Path:
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("snapshot filename is required.")
    if not SNAPSHOT_FILENAME_RE.match(cleaned):
        raise ValueError("Invalid snapshot filename.")
    if not cleaned.endswith(".json"):
        raise ValueError("snapshot filename must end with .json.")
    return SNAPSHOT_DIR / cleaned


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


def _load_orchestrator_schema() -> Dict[str, object]:
    global _ORCHESTRATOR_SCHEMA_CACHE
    if _ORCHESTRATOR_SCHEMA_CACHE is not None:
        return _ORCHESTRATOR_SCHEMA_CACHE

    if not CONSOLIDATED_SYSTEM_MESSAGES_PATH.exists():
        raise FileNotFoundError(f"{CONSOLIDATED_SYSTEM_MESSAGES_PATH.name} is missing")

    text = CONSOLIDATED_SYSTEM_MESSAGES_PATH.read_text(encoding="utf-8")
    marker = f"# {ORCHESTRATOR_SCHEMA_HEADING}"
    index = text.find(marker)
    if index == -1:
        raise KeyError(f"Heading not found: {ORCHESTRATOR_SCHEMA_HEADING}")

    snippet = text[index:]
    match = re.search(r"```json\s*(.*?)\s*```", snippet, re.S)
    if not match:
        raise ValueError("Orchestrator schema JSON block not found.")

    schema_text = match.group(1)
    try:
        _ORCHESTRATOR_SCHEMA_CACHE = json.loads(schema_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid orchestrator schema JSON: {exc.msg}") from exc

    return _ORCHESTRATOR_SCHEMA_CACHE


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


def create_orchestrator_response(
    messages: List[Dict[str, object]],
    *,
    model: str,
    text_verbosity: str,
    reasoning_effort: str,
    background: bool,
) -> object:
    """Invoke Responses API with JSON schema output for the orchestrator stage."""

    schema = _load_orchestrator_schema()
    text_config: Dict[str, object] = {
        "format": {
            "type": "json_schema",
            "name": "orchestrator_decision",
            "strict": True,
            "schema": schema,
        }
    }
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


def _extract_output_texts(response) -> List[str]:
    """Extract raw output_text blocks for JSON parsing."""

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


def _parse_output_json(texts: List[str]) -> tuple[List[object], List[str]]:
    parsed: List[object] = []
    errors: List[str] = []
    for index, text in enumerate(texts, start=1):
        try:
            parsed.append(json.loads(text))
        except json.JSONDecodeError as exc:
            errors.append(f"output_text[{index}] JSON error: {exc.msg}")
    return parsed, errors


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

PROMPT_HTML_PATH = Path(__file__).resolve().parent / "prompt_agent.html"
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


@app.get("/api/agentic-state")
def get_agentic_state():
    filename = request.args.get("filename")
    try:
        state_path = _resolve_state_path(filename)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400
    if not state_path.exists():
        return jsonify(ok=False, error="No saved state found."), 404
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return jsonify(ok=False, error=f"Saved state is invalid JSON: {exc.msg}"), 500
    return jsonify(ok=True, state=state)


@app.post("/api/agentic-state")
def save_agentic_state():
    payload = request.get_json(silent=True) or {}
    filename = payload.get("filename") or request.args.get("filename")
    if filename is not None and not isinstance(filename, str):
        return jsonify(ok=False, error="filename must be a string."), 400
    try:
        state_path = _resolve_state_path(filename)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400
    state = payload.get("state")
    if not isinstance(state, dict):
        return jsonify(ok=False, error="state must be an object."), 400
    try:
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:
        app.logger.exception("Failed to write agentic state")
        return jsonify(ok=False, error=str(exc)), 500
    return jsonify(ok=True)


@app.get("/api/agentic-snapshots")
def list_agentic_snapshots():
    filename = request.args.get("filename")
    try:
        base_name = _normalize_state_filename(filename)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    base_stem = Path(base_name).stem
    prefix = f"{base_stem}_"

    _ensure_snapshot_dir()
    snapshots = []
    for path in SNAPSHOT_DIR.glob(f"{prefix}*.json"):
        if not SNAPSHOT_FILENAME_RE.match(path.name):
            continue
        meta: Dict[str, object] = {"filename": path.name}
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            state = None
        if isinstance(state, dict):
            meta["saved_at"] = state.get("saved_at")
            meta["note"] = state.get("note")
            workflow = state.get("workflow")
            if isinstance(workflow, dict):
                meta["loop_count"] = workflow.get("loopCount")
                meta["last_stage"] = workflow.get("lastStage")
        try:
            meta["mtime"] = path.stat().st_mtime
        except OSError:
            meta["mtime"] = 0
        snapshots.append(meta)

    snapshots.sort(key=lambda item: item.get("mtime", 0), reverse=True)
    for item in snapshots:
        item.pop("mtime", None)

    return jsonify(ok=True, snapshots=snapshots)


@app.get("/api/agentic-snapshot")
def get_agentic_snapshot():
    name = request.args.get("name") or request.args.get("filename")
    if not isinstance(name, str):
        return jsonify(ok=False, error="snapshot filename is required."), 400

    try:
        snapshot_path = _resolve_snapshot_name(name)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    if not snapshot_path.exists():
        return jsonify(ok=False, error="Snapshot not found."), 404

    try:
        state = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return jsonify(ok=False, error=f"Snapshot is invalid JSON: {exc.msg}"), 500

    return jsonify(ok=True, state=state, filename=snapshot_path.name)


@app.post("/api/agentic-snapshot")
def save_agentic_snapshot():
    payload = request.get_json(silent=True) or {}
    filename = payload.get("filename") or request.args.get("filename")
    label = payload.get("label")
    state = payload.get("state")

    if filename is not None and not isinstance(filename, str):
        return jsonify(ok=False, error="filename must be a string."), 400
    if not isinstance(state, dict):
        return jsonify(ok=False, error="state must be an object."), 400

    try:
        snapshot_path = _resolve_snapshot_path(filename, label)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400

    _ensure_snapshot_dir()
    try:
        snapshot_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError as exc:
        app.logger.exception("Failed to write snapshot state")
        return jsonify(ok=False, error=str(exc)), 500

    return jsonify(ok=True, filename=snapshot_path.name)


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


@app.post("/api/orchestrator-run")
def handle_orchestrator_run():
    payload = request.get_json(silent=True) or {}

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
        response = create_orchestrator_response(
            messages,
            model=model,
            text_verbosity=text_verbosity or "high",
            reasoning_effort=reasoning_effort or "high",
            background=False,
        )
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Orchestrator response creation failed")
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


@app.post("/api/orchestrator-run-background")
def handle_orchestrator_run_background():
    payload = request.get_json(silent=True) or {}

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
        response = create_orchestrator_response(
            messages,
            model=model,
            text_verbosity=text_verbosity or "high",
            reasoning_effort=reasoning_effort or "high",
            background=True,
        )
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background orchestrator creation failed")
        return jsonify(ok=False, error=str(exc)), 500

    return jsonify(
        ok=True,
        response_id=response.id,
        status=response.status,
        response=response.model_dump(),
    )


@app.get("/api/orchestrator-run-background/<response_id>")
def poll_orchestrator_run(response_id: str):
    try:
        response = client.responses.retrieve(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background orchestrator polling failed")
        return jsonify(ok=False, error=str(exc)), 500

    output_texts = _extract_output_texts(response)
    parsed_outputs, parse_errors = _parse_output_json(output_texts)

    payload = {
        "ok": True,
        "status": response.status,
        "response": response.model_dump(),
        "output_texts": output_texts,
        "parsed_outputs": parsed_outputs,
        "parse_errors": parse_errors,
    }
    payload["done"] = response.status in {"completed", "failed", "cancelled"}
    return jsonify(payload)


@app.post("/api/orchestrator-run-background/<response_id>/cancel")
def cancel_orchestrator_run(response_id: str):
    if not response_id:
        return jsonify(ok=False, error="response_id is required."), 400

    try:
        response = client.responses.cancel(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background orchestrator cancellation failed")
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
    port = int(os.getenv("TRY_SERVER_PORT", "2357"))
    app.run(host=host, port=port, debug=os.getenv("FLASK_DEBUG") == "1")
