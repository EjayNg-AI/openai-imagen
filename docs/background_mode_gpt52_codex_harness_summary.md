# Background-Mode OpenAI API Test from the Codex Harness

## Session Summary

In the previous coding session, we validated an end-to-end workflow for running a local Python script from inside the Codex harness. The script sends an OpenAI Responses API request in **background mode**, then polls for status updates until completion.

The tested command was:

```bash
python -u scratchpad/background_mode_gpt52_test.py
```

Key behaviors confirmed:

- The script submits a complex prompt to `gpt-5.2` using `background=True`.
- The script polls every 10 seconds (`GET /v1/responses/{response_id}`) until it reaches a terminal status.
- Progress is emitted to the terminal in real time.
- The script writes a structured Markdown report to `scratchpad/background_mode_gpt52_test_report.md` containing run config, event log, final output, and raw JSON payload.

## Why `-u` Matters for Real-Time Status in Codex

Running Python with the `-u` flag enables unbuffered stdout/stderr. In this workflow, that is important because:

- Polling status updates are visible immediately in the terminal.
- You can monitor long-running background jobs without waiting for buffered flushes.
- Logs in the Codex harness better reflect actual progress timing.

Without `-u`, line buffering can delay visible output depending on runtime and environment.

## Script Flow (What It Does)

1. Loads environment variables and validates `OPENAI_API_KEY`.
2. Initializes report header metadata (model, reasoning effort, polling interval, prompt used).
3. Submits a background-mode request via `POST /v1/responses`.
4. Polls response status via `GET /v1/responses/{response_id}` every 10 seconds.
5. Logs each poll both to console and to report markdown.
6. On terminal status, appends:
   - final status metadata,
   - extracted assistant text output,
   - full raw response JSON.

Terminal states handled by the script: `completed`, `failed`, `cancelled`, `incomplete`, `expired`.

## Outbound Network Access Guidance and Allowlisting

From the Codex harness perspective, two network paths are relevant:

- Built-in browsing tools run in the harness tool environment.
- Local scripts (like this Python file) run in the workspace process sandbox and require outbound network access from that runtime.

That means web browsing may work while local API calls still fail if workspace outbound policy blocks the call.

OpenAI guidance emphasizes least-privilege outbound access. For this script, the minimal policy is:

- Allowlisted domain: `api.openai.com`
- Required HTTP methods:
  - `POST` for `POST /v1/responses`
  - `GET` for `GET /v1/responses/{response_id}` polling
- Optional method/path:
  - `POST /v1/responses/{response_id}/cancel` if cancellation is needed

If outbound rules only allow `GET/HEAD/OPTIONS`, request creation fails because `POST` is required.

Reference notes source: `docs/codex_outbound_network_access.md`.

## Full Script Copy: `scratchpad/background_mode_gpt52_test.py`

```python
#!/usr/bin/env python3
"""Background-mode Responses API smoke test for gpt-5.2.

This script:
1. Submits a deliberately complex prompt using background mode.
2. Polls the response every 10 seconds (configurable).
3. Writes status updates, logs, and final output to a Markdown report file.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_MODEL = "gpt-5.2"
DEFAULT_POLL_INTERVAL_SECONDS = 10
DEFAULT_REPORT_PATH = "scratchpad/background_mode_gpt52_test_report.md"
TERMINAL_STATUSES = {"completed", "failed", "cancelled", "incomplete", "expired"}

COMPLEX_QUESTION = """
Solve the following integrated planning and algorithm design challenge.

A startup must schedule 12 engineering tasks with precedence and limited staffing.
Each task has (duration, predecessors, delay penalty weight):
- A: (4, -, 8)
- B: (3, A, 4)
- C: (5, A, 7)
- D: (6, A, 9)
- E: (2, B, 5)
- F: (4, B,C, 6)
- G: (3, C, 3)
- H: (7, D, 10)
- I: (2, E,F, 5)
- J: (5, F,G, 7)
- K: (4, H,I, 8)
- L: (3, J,K, 9)

Resource constraints:
- Team Alpha can run at most 2 tasks concurrently.
- Team Beta can run at most 1 task concurrently.
- Tasks D, H, K require Team Beta.
- All other tasks require Team Alpha.

Project deadline target is day 22. Objective is to minimize weighted tardiness
sum(weight_i * max(0, completion_i - due_i)), with due_i set to 22 for all tasks.

Please do all of the following:
1. Compute an earliest-start schedule and identify the critical path.
2. Formulate a mixed-integer optimization model with clear variables,
   objective, precedence constraints, and resource-capacity constraints.
3. Propose one feasible near-optimal schedule and justify quality using a
   lower bound argument (for example, relaxation or bottleneck-based bound).
4. Provide pseudocode for a branch-and-bound strategy with a greedy warm start.
5. Analyze time complexity and where pruning is expected to help in practice.
6. Perform sensitivity analysis for two what-if changes:
   - duration(F) increases from 4 to 6
   - duration(H) decreases from 7 to 5
7. Summarize recommended schedule strategy for an engineering manager.

Return the final answer in well-structured Markdown with equations and at least
one table.
""".strip()

DEVELOPER_INSTRUCTION = (
    "You are a rigorous operations research assistant. Provide a complete, "
    "careful solution and clearly label assumptions."
)


def utc_now() -> str:
    """Return a compact UTC timestamp for logs."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def append_text(path: Path, text: str) -> None:
    """Append UTF-8 text to a report file."""
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def write_report_header(path: Path, model: str, poll_interval: int) -> None:
    """Initialize the markdown report with run metadata and prompt."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# GPT-5.2 Background Mode Test Report",
                "",
                "## Run Configuration",
                f"- `started_at_utc`: `{utc_now()}`",
                f"- `model`: `{model}`",
                "- `reasoning.effort`: `high`",
                "- `background`: `true`",
                f"- `poll_interval_seconds`: `{poll_interval}`",
                "",
                "## Prompt Used",
                "```text",
                COMPLEX_QUESTION,
                "```",
                "",
                "## Event Log",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_event(path: Path, level: str, message: str) -> None:
    """Write one timestamped log event to markdown."""
    append_text(path, f"- `{utc_now()}` `{level.upper()}` {message}\n")


def response_to_dict(response: Any) -> Any:
    """Best-effort conversion of a response object into JSON-serializable data."""
    if hasattr(response, "model_dump"):
        try:
            return response.model_dump()
        except Exception:
            pass
    if hasattr(response, "to_dict"):
        try:
            return response.to_dict()
        except Exception:
            pass
    return {"raw_repr": repr(response)}


def extract_output_text(response: Any) -> str:
    """Collect assistant output text from response."""
    direct_text = getattr(response, "output_text", None)
    if isinstance(direct_text, str) and direct_text.strip():
        return direct_text.strip()

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


def append_final_sections(path: Path, response: Any, status: str, response_id: str) -> None:
    """Append final status, output text, and raw response JSON to report."""
    append_text(
        path,
        "\n".join(
            [
                "",
                "## Final Status",
                f"- `response_id`: `{response_id}`",
                f"- `status`: `{status}`",
                f"- `finished_at_utc`: `{utc_now()}`",
                "",
            ]
        ),
    )

    model_output = extract_output_text(response)
    append_text(path, "## Final Model Output\n")
    if model_output:
        append_text(path, "```text\n")
        append_text(path, model_output + "\n")
        append_text(path, "```\n")
    else:
        append_text(path, "_No `output_text` found in response payload._\n")

    raw = response_to_dict(response)
    append_text(path, "\n## Final Response Payload\n")
    append_text(path, "```json\n")
    append_text(path, json.dumps(raw, indent=2, ensure_ascii=True, default=str))
    append_text(path, "\n```\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run a background-mode GPT-5.2 test request and write status and "
            "final output to a Markdown file."
        )
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name (default: gpt-5.2).")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help="Polling interval in seconds (default: 10).",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_REPORT_PATH,
        help="Markdown report output path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.poll_interval <= 0:
        print("poll interval must be a positive integer", file=sys.stderr)
        return 2

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger("background_mode_gpt52_test")

    report_path = Path(args.output).expanduser()
    write_report_header(report_path, model=args.model, poll_interval=args.poll_interval)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        msg = "OPENAI_API_KEY is not set. Aborting run."
        logger.error(msg)
        write_event(report_path, "error", msg)
        return 1

    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "developer",
            "content": [{"type": "input_text", "text": DEVELOPER_INSTRUCTION}],
        },
        {
            "role": "user",
            "content": [{"type": "input_text", "text": COMPLEX_QUESTION}],
        },
    ]

    write_event(report_path, "info", "Submitting background request.")
    logger.info("Submitting background request to model=%s", args.model)

    try:
        create_resp = client.responses.create(
            model=args.model,
            input=messages,
            text={"format": {"type": "text"}, "verbosity": "high"},
            reasoning={"effort": "high", "summary": None},
            background=True,
        )
    except Exception as exc:
        err = f"Request submission failed: {exc}"
        logger.exception(err)
        write_event(report_path, "error", err)
        return 1

    response_id = getattr(create_resp, "id", "")
    status = getattr(create_resp, "status", "unknown")
    logger.info("Background task started: id=%s status=%s", response_id, status)
    write_event(
        report_path,
        "info",
        f"Background task started with `response_id={response_id}` and initial `status={status}`.",
    )

    latest = create_resp
    poll_count = 0

    try:
        while status not in TERMINAL_STATUSES:
            time.sleep(args.poll_interval)
            poll_count += 1
            latest = client.responses.retrieve(response_id)
            status = getattr(latest, "status", "unknown")
            logger.info("Poll %s: status=%s", poll_count, status)
            write_event(report_path, "info", f"poll={poll_count} status=`{status}`")
    except Exception as exc:
        err = f"Polling failed after {poll_count} polls: {exc}"
        logger.exception(err)
        write_event(report_path, "error", err)
        return 1

    write_event(
        report_path,
        "info",
        f"Terminal status reached after {poll_count} polls: `{status}`.",
    )
    logger.info("Terminal status reached: %s", status)

    append_final_sections(report_path, response=latest, status=status, response_id=response_id)

    print(f"Report written to: {report_path}")
    print(f"Final status: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```
