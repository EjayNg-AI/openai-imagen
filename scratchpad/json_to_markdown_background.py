#!/usr/bin/env python3
"""Submit JSON data to the OpenAI Responses API (background mode) and save Markdown output.

Usage example:
python -u scratchpad/json_to_markdown_background.py \
  --input-json-file /path/to/input.json \
  --output-markdown-file scratchpad/openclaw_report.md \
  --model gpt-5.2 \
  --reasoning-effort high \
  --verbosity high
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


TERMINAL_STATUSES = {"completed", "failed", "cancelled", "expired", "incomplete"}
DEFAULT_DEVELOPER_INSTRUCTIONS = (
    "You are a careful research analyst. Given JSON records from the user, treat them as a "
    "provided collection of research outputs and produce a complete, well-structured Markdown "
    "report. Deduplicate repetition without losing unique details. Call out ambiguities and "
    "contradictions, reconcile when possible, and cite web findings when you use web search."
)
DEFAULT_USER_TASK = (
    "Analyze the following provided research collection (JSON records) and return Markdown only.\n\n"
    "The report must be comprehensive and include all details, including minor points.\n"
    "When there are contradictions or ambiguities, explicitly reconcile them.\n"
    "If the provided records are insufficient, use web search and explain how external evidence was used."
)


def _configure_line_buffering() -> None:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass


def _emit(event: str, **fields: Any) -> None:
    payload: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event,
    }
    payload.update(fields)
    print(json.dumps(payload, ensure_ascii=True), flush=True)


def _load_json_from_file(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to read JSON file {path}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc


def _to_plain_json(response: Any) -> dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()  # type: ignore[no-any-return]
    if hasattr(response, "model_dump_json"):
        return json.loads(response.model_dump_json())  # type: ignore[no-any-return]
    if hasattr(response, "to_dict"):
        return response.to_dict()  # type: ignore[no-any-return]
    return {"repr": repr(response)}


def _extract_output_text(response: Any) -> str:
    direct = getattr(response, "output_text", None)
    if isinstance(direct, str) and direct.strip():
        return direct.strip()

    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for block in getattr(item, "content", []) or []:
            if getattr(block, "type", None) != "output_text":
                continue
            text = getattr(block, "text", None)
            if isinstance(text, str) and text.strip():
                chunks.append(text.strip())
    return "\n\n".join(chunks).strip()


def _build_messages(developer_instructions: str, user_task: str, input_data: Any) -> list[dict[str, Any]]:
    json_blob = json.dumps(input_data, indent=2, ensure_ascii=False)
    user_text = (
        f"{user_task}\n\n"
        "Input JSON:\n"
        "```json\n"
        f"{json_blob}\n"
        "```"
    )
    return [
        {
            "role": "developer",
            "content": [{"type": "input_text", "text": developer_instructions}],
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": user_text}],
        },
    ]


def _poll_to_terminal(
    client: OpenAI,
    response_id: str,
    poll_seconds: float,
    max_wait_seconds: int,
) -> Any:
    started = time.monotonic()
    attempt = 0

    while True:
        attempt += 1
        response = client.responses.retrieve(response_id)
        status = getattr(response, "status", "unknown")
        elapsed_seconds = int(time.monotonic() - started)
        _emit(
            "poll",
            response_id=response_id,
            attempt=attempt,
            status=status,
            elapsed_seconds=elapsed_seconds,
        )

        if status in TERMINAL_STATUSES:
            return response

        if max_wait_seconds > 0 and elapsed_seconds >= max_wait_seconds:
            raise TimeoutError(
                f"Polling timed out after {elapsed_seconds} seconds (max {max_wait_seconds})."
            )

        time.sleep(poll_seconds)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Pass JSON input to a model using Responses API background mode and save Markdown output."
        )
    )
    parser.add_argument(
        "--input-json-file",
        required=True,
        help="Path to input JSON file.",
    )
    parser.add_argument(
        "--output-markdown-file",
        default="scratchpad/model_output.md",
        help="Path for final markdown output (default: scratchpad/model_output.md).",
    )
    parser.add_argument(
        "--output-response-json-file",
        default="",
        help="Optional path to save final raw response JSON payload.",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2).",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh"),
        default="high",
        help="Reasoning effort (default: high).",
    )
    parser.add_argument(
        "--verbosity",
        choices=("low", "medium", "high"),
        default="high",
        help="Text verbosity (default: high).",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=10.0,
        help="Polling interval in seconds (default: 10).",
    )
    parser.add_argument(
        "--max-wait-seconds",
        type=int,
        default=0,
        help="Maximum wait time in seconds, 0 disables timeout (default: 0).",
    )
    parser.add_argument(
        "--search-context-size",
        choices=("low", "medium", "high"),
        default="high",
        help="web_search tool context size (default: high).",
    )
    parser.add_argument(
        "--developer-instructions-file",
        default="",
        help="Optional path to developer instructions text file.",
    )
    parser.add_argument(
        "--user-task-file",
        default="",
        help="Optional path to user task text file.",
    )
    return parser


def _read_optional_text_file(path_str: str, default_value: str) -> str:
    if not path_str:
        return default_value
    path = Path(path_str)
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise RuntimeError(f"Failed to read text file {path}: {exc}") from exc
    if not content:
        raise RuntimeError(f"Text file is empty: {path}")
    return content


def main() -> int:
    _configure_line_buffering()
    parser = _build_parser()
    args = parser.parse_args()

    if args.poll_seconds <= 0:
        parser.error("--poll-seconds must be greater than 0.")
    if args.max_wait_seconds < 0:
        parser.error("--max-wait-seconds must be >= 0.")

    try:
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set. Add it to environment or .env file.")

        input_path = Path(args.input_json_file)
        input_data = _load_json_from_file(input_path)
        developer_instructions = _read_optional_text_file(
            args.developer_instructions_file,
            DEFAULT_DEVELOPER_INSTRUCTIONS,
        )
        user_task = _read_optional_text_file(args.user_task_file, DEFAULT_USER_TASK)

        messages = _build_messages(
            developer_instructions=developer_instructions,
            user_task=user_task,
            input_data=input_data,
        )

        _emit(
            "submit_start",
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            verbosity=args.verbosity,
            poll_seconds=args.poll_seconds,
            input_json_file=str(input_path),
        )

        client = OpenAI()
        created = client.responses.create(
            model=args.model,
            input=messages,
            text={"format": {"type": "text"}, "verbosity": args.verbosity},
            reasoning={"effort": args.reasoning_effort},
            tools=[
                {
                    "type": "web_search",
                    "user_location": {"type": "approximate"},
                    "search_context_size": args.search_context_size,
                }
            ],
            background=True,
        )

        response_id = getattr(created, "id", None)
        if not response_id:
            raise RuntimeError("Responses API did not return a response id.")

        _emit("submitted", response_id=response_id, status=getattr(created, "status", "unknown"))

        final_response = _poll_to_terminal(
            client=client,
            response_id=response_id,
            poll_seconds=args.poll_seconds,
            max_wait_seconds=args.max_wait_seconds,
        )
        final_status = getattr(final_response, "status", "unknown")
        _emit("final", response_id=response_id, status=final_status)

        if args.output_response_json_file:
            response_path = Path(args.output_response_json_file)
            response_path.parent.mkdir(parents=True, exist_ok=True)
            response_path.write_text(
                json.dumps(_to_plain_json(final_response), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            _emit("wrote_response_json", path=str(response_path))

        markdown_text = _extract_output_text(final_response)
        if final_status == "completed" and not markdown_text:
            raise RuntimeError("Completed response has no output_text content.")

        markdown_path = Path(args.output_markdown_file)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(markdown_text, encoding="utf-8")
        _emit("wrote_markdown", path=str(markdown_path), chars=len(markdown_text))

        return 0 if final_status == "completed" else 2
    except TimeoutError as exc:
        _emit("timeout", message=str(exc))
        return 3
    except KeyboardInterrupt:
        _emit("cancelled_by_user")
        return 130
    except Exception as exc:
        _emit("error", error_type=type(exc).__name__, message=str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
