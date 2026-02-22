#!/usr/bin/env python3
"""Assemble topic threads from archive data and generate a background markdown report."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


TERMINAL_STATUSES = {"completed", "failed", "cancelled", "expired", "incomplete"}
ARCHIVE_NAME_RE = re.compile(r"^chatgpt_conversation_history_(\d{4}-\d{2}-\d{2})$")
DEFAULT_USER_TASK = (
    "Analyze the provided JSON dataset about {{TOPIC}} and produce a comprehensive markdown report. "
    "Follow developer instructions exactly. Return markdown only."
)


@dataclass(frozen=True)
class ArchiveInfo:
    path: Path
    archive_date: date | None


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def status_line(message: str) -> None:
    print(f"[{utc_now_iso()}] {message}", flush=True)


def _configure_line_buffering() -> None:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(line_buffering=True)
    except Exception:
        pass


def parse_archive_date(folder_name: str) -> date | None:
    match = ARCHIVE_NAME_RE.match(folder_name)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def discover_archives(sites_root: Path) -> list[ArchiveInfo]:
    if not sites_root.exists():
        raise RuntimeError(f"Sites root does not exist: {sites_root}")

    archives: list[ArchiveInfo] = []
    for entry in sites_root.iterdir():
        if not entry.is_dir():
            continue
        archive_date = parse_archive_date(entry.name)
        if archive_date is None:
            continue
        if not (entry / "viewer_data" / "index.json").exists():
            continue
        if not (entry / "viewer_data" / "conversations").is_dir():
            continue
        archives.append(ArchiveInfo(path=entry, archive_date=archive_date))

    if not archives:
        raise RuntimeError(f"No valid archive folders found under: {sites_root}")

    archives.sort(key=lambda a: (a.archive_date or date.min, a.path.name))
    return archives


def select_archives(archives: list[ArchiveInfo], scope: str) -> list[ArchiveInfo]:
    if scope == "latest":
        return [archives[-1]]
    return list(archives)


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "topic"


def _is_probably_noise_word(word: str) -> bool:
    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "about",
        "into",
        "latest",
        "chatgpt",
        "thread",
        "threads",
        "topic",
        "report",
        "analysis",
    }
    return word in stopwords


def build_keyword_regex(topic: str, keyword_regex: str, extra_keywords: list[str]) -> tuple[re.Pattern[str], list[str], str]:
    if keyword_regex.strip():
        try:
            compiled = re.compile(keyword_regex, re.IGNORECASE)
        except re.error as exc:
            raise RuntimeError(f"Invalid --keyword-regex: {exc}") from exc
        return compiled, [], keyword_regex

    terms: list[str] = []

    split_terms = [part.strip() for part in re.split(r"[\\/|,;]+", topic) if part.strip()]
    if split_terms:
        terms.extend(split_terms)
    elif topic.strip():
        terms.append(topic.strip())

    if len(split_terms) <= 1:
        for word in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{2,}", topic):
            low = word.lower()
            if _is_probably_noise_word(low):
                continue
            terms.append(word)

    for keyword in extra_keywords:
        kw = keyword.strip()
        if kw:
            terms.append(kw)

    dedup_terms: list[str] = []
    seen: set[str] = set()
    for term in terms:
        key = term.lower()
        if key in seen:
            continue
        seen.add(key)
        dedup_terms.append(term)

    if not dedup_terms:
        raise RuntimeError("Could not build keyword terms. Provide --keyword or --keyword-regex.")

    pattern = "|".join(re.escape(term) for term in dedup_terms)
    return re.compile(pattern, re.IGNORECASE), dedup_terms, pattern


def ts_to_utc_iso(ts: Any) -> str | None:
    if not isinstance(ts, (int, float)):
        return None
    return datetime.fromtimestamp(ts, UTC).isoformat(timespec="seconds")


def _extract_text_from_parts(parts: Any) -> str:
    chunks: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, str):
            text = value.strip()
            if text:
                chunks.append(text)
            return
        if isinstance(value, list):
            for item in value:
                walk(item)
            return
        if isinstance(value, dict):
            if isinstance(value.get("text"), str):
                walk(value.get("text"))
            if isinstance(value.get("title"), str):
                walk(value.get("title"))
            for key, nested in value.items():
                if key in {"text", "title"}:
                    continue
                if isinstance(nested, (str, list, dict)):
                    walk(nested)

    walk(parts)
    return re.sub(r"\s+", " ", " ".join(chunks)).strip()


def _collect_visible_messages(conversation: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return []

    messages: list[dict[str, Any]] = []
    for node in mapping.values():
        if not isinstance(node, dict):
            continue
        msg = node.get("message")
        if not isinstance(msg, dict):
            continue

        metadata = msg.get("metadata")
        if isinstance(metadata, dict) and metadata.get("is_visually_hidden_from_conversation") is True:
            continue

        author = msg.get("author")
        role = author.get("role") if isinstance(author, dict) else None
        if role not in {"user", "assistant", "tool", "system"}:
            continue

        content = msg.get("content")
        if not isinstance(content, dict):
            continue
        text = _extract_text_from_parts(content.get("parts"))
        if not text:
            continue

        messages.append(
            {
                "id": msg.get("id"),
                "role": role,
                "create_time": msg.get("create_time"),
                "create_time_utc": ts_to_utc_iso(msg.get("create_time")),
                "text": text,
            }
        )

    def sort_key(item: dict[str, Any]) -> tuple[float, str]:
        ts = item.get("create_time")
        ts_float = float(ts) if isinstance(ts, (int, float)) else -1.0
        return ts_float, str(item.get("id") or "")

    messages.sort(key=sort_key)

    seen_ids: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for item in messages:
        msg_id = item.get("id")
        if isinstance(msg_id, str) and msg_id:
            if msg_id in seen_ids:
                continue
            seen_ids.add(msg_id)
        deduped.append(item)
    return deduped


def _load_index(index_path: Path) -> dict[str, dict[str, Any]]:
    rows = json.loads(index_path.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                out[row["id"]] = row
    return out


def assemble_topic_dataset(
    selected_archives: list[ArchiveInfo],
    topic: str,
    keyword_pattern: re.Pattern[str],
    keyword_pattern_raw: str,
    keyword_terms: list[str],
    scope: str,
    max_messages_per_thread: int,
) -> dict[str, Any]:
    best_by_id: dict[str, dict[str, Any]] = {}

    for archive in selected_archives:
        idx_path = archive.path / "viewer_data" / "index.json"
        conv_dir = archive.path / "viewer_data" / "conversations"
        index = _load_index(idx_path)

        for conv_file in conv_dir.glob("*.json"):
            raw = conv_file.read_text(encoding="utf-8", errors="ignore")
            if not keyword_pattern.search(raw):
                continue

            conversation_id = conv_file.stem
            meta = index.get(conversation_id, {})
            update_time = meta.get("update_time")
            update_sort = float(update_time) if isinstance(update_time, (int, float)) else -1.0

            candidate = {
                "archive": archive.path.name,
                "conversation_path": str(conv_file),
                "conversation_id": conversation_id,
                "meta": {
                    "title": meta.get("title"),
                    "create_time": meta.get("create_time"),
                    "create_time_utc": ts_to_utc_iso(meta.get("create_time")),
                    "update_time": meta.get("update_time"),
                    "update_time_utc": ts_to_utc_iso(meta.get("update_time")),
                    "message_count": meta.get("message_count"),
                    "node_count": meta.get("node_count"),
                },
                "raw": raw,
                "update_sort": update_sort,
            }

            prev = best_by_id.get(conversation_id)
            if prev is None or candidate["update_sort"] > prev["update_sort"]:
                best_by_id[conversation_id] = candidate

    direct_threads: list[dict[str, Any]] = []
    incidental_mentions: list[dict[str, Any]] = []

    for rec in sorted(best_by_id.values(), key=lambda x: x["update_sort"], reverse=True):
        conversation = json.loads(rec["raw"])
        visible_messages = _collect_visible_messages(conversation)

        title = str(rec["meta"].get("title") or "")
        title_match = bool(keyword_pattern.search(title))

        keyword_hits: list[dict[str, Any]] = []
        role_hits: set[str] = set()
        for idx, message in enumerate(visible_messages):
            text = str(message.get("text") or "")
            if not keyword_pattern.search(text):
                continue
            role = str(message.get("role") or "")
            role_hits.add(role)
            keyword_hits.append(
                {
                    "message_index": idx,
                    "role": role,
                    "create_time_utc": message.get("create_time_utc"),
                    "text": text,
                }
            )

        is_direct = title_match or bool(role_hits.intersection({"user", "assistant", "tool"}))

        base = {
            "conversation_id": rec["conversation_id"],
            "archive": rec["archive"],
            "conversation_path": rec["conversation_path"],
            "meta": rec["meta"],
            "title_match": title_match,
            "visible_message_count": len(visible_messages),
            "keyword_hit_count_in_visible_messages": len(keyword_hits),
            "keyword_hits": keyword_hits,
        }

        if is_direct:
            messages = visible_messages
            truncated = False
            if max_messages_per_thread > 0 and len(messages) > max_messages_per_thread:
                messages = messages[:max_messages_per_thread]
                truncated = True
            entry = dict(base)
            entry["classification"] = "direct_topic_thread"
            entry["messages"] = messages
            entry["messages_truncated"] = truncated
            direct_threads.append(entry)
        else:
            entry = dict(base)
            entry["classification"] = "incidental_mention"
            entry["sample_keyword_contexts"] = keyword_hits[:3]
            incidental_mentions.append(entry)

    return {
        "topic": topic,
        "assembled_at_utc": utc_now_iso(),
        "archive_scope": scope,
        "selected_archives": [a.path.name for a in selected_archives],
        "keyword_regex": keyword_pattern_raw,
        "keyword_terms": keyword_terms,
        "deduplication_policy": "Conversation IDs deduplicated by latest update_time across selected archives.",
        "summary": {
            "matched_conversation_ids": len(best_by_id),
            "direct_topic_threads": len(direct_threads),
            "incidental_mentions": len(incidental_mentions),
        },
        "conversations": {
            "direct_topic_threads": direct_threads,
            "incidental_mentions": incidental_mentions,
        },
    }


def _read_text_file(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Failed to read file {path}: {exc}") from exc
    if not text.strip():
        raise RuntimeError(f"File is empty: {path}")
    return text


def _load_developer_prompt(template_path: Path, topic: str, ad_hoc_requirements: str) -> str:
    template = _read_text_file(template_path)
    if "{{TOPIC}}" in template:
        prompt = template.replace("{{TOPIC}}", topic)
    else:
        prompt = f"{template.rstrip()}\n\nTopic: {topic}\n"
    if ad_hoc_requirements.strip():
        prompt = (
            f"{prompt.rstrip()}\n\n"
            "Additional run-specific requirements:\n"
            f"{ad_hoc_requirements.strip()}\n"
        )
    return prompt.strip() + "\n"


def _load_user_task(task_file: Path | None, topic: str, ad_hoc_requirements: str) -> str:
    if task_file is None:
        base = DEFAULT_USER_TASK
    else:
        base = _read_text_file(task_file)

    if "{{TOPIC}}" in base:
        task = base.replace("{{TOPIC}}", topic)
    else:
        task = f"{base.rstrip()}\n\nTopic: {topic}\n"

    if ad_hoc_requirements.strip():
        task = (
            f"{task.rstrip()}\n\n"
            "Additional requirements:\n"
            f"{ad_hoc_requirements.strip()}\n"
        )

    return task.strip() + "\n"


def _combine_ad_hoc_requirements(inline_value: str, file_path: Path | None) -> str:
    parts: list[str] = []
    if inline_value.strip():
        parts.append(inline_value.strip())
    if file_path is not None:
        parts.append(_read_text_file(file_path).strip())
    return "\n\n".join(part for part in parts if part)


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


def _to_plain_json(response: Any) -> dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()  # type: ignore[no-any-return]
    if hasattr(response, "model_dump_json"):
        return json.loads(response.model_dump_json())  # type: ignore[no-any-return]
    if hasattr(response, "to_dict"):
        return response.to_dict()  # type: ignore[no-any-return]
    return {"repr": repr(response)}


def poll_background(
    client: OpenAI,
    response_id: str,
    poll_seconds: float,
    max_wait_seconds: int,
    heartbeat_seconds: int,
    verbose_poll: bool,
) -> Any:
    started = time.monotonic()
    last_status: str | None = None
    last_print_elapsed = -1
    attempt = 0

    while True:
        attempt += 1
        response = client.responses.retrieve(response_id)
        status = getattr(response, "status", "unknown")
        elapsed = int(time.monotonic() - started)

        should_print = False
        if verbose_poll:
            should_print = True
        elif status != last_status:
            should_print = True
        elif heartbeat_seconds > 0 and elapsed - last_print_elapsed >= heartbeat_seconds:
            should_print = True

        if should_print:
            status_line(f"poll attempt={attempt} status={status} elapsed={elapsed}s")
            last_print_elapsed = elapsed

        last_status = status
        if status in TERMINAL_STATUSES:
            return response

        if max_wait_seconds > 0 and elapsed >= max_wait_seconds:
            raise TimeoutError(
                f"Timed out after {elapsed} seconds while waiting for response {response_id}."
            )

        time.sleep(poll_seconds)


def build_parser() -> argparse.ArgumentParser:
    script_dir = Path(__file__).resolve().parent
    default_prompt_template = (
        script_dir.parent / "references" / "developer_prompt_template.txt"
    )

    parser = argparse.ArgumentParser(
        description="Assemble archive topic data and generate a background markdown report."
    )
    parser.add_argument("--topic", required=True, help="Topic to search for.")
    parser.add_argument(
        "--archive-scope",
        choices=("latest", "all"),
        default="latest",
        help="Search latest archive only or all archives (default: latest).",
    )
    parser.add_argument(
        "--sites-root",
        default="chatgpt_viewer_sites",
        help="Root directory containing archive folders.",
    )
    parser.add_argument(
        "--output-root",
        default="scratchpad/topic_background_reports",
        help="Directory where run artifacts are saved.",
    )
    parser.add_argument(
        "--keyword-regex",
        default="",
        help="Optional regex override for thread matching.",
    )
    parser.add_argument(
        "--keyword",
        action="append",
        default=[],
        help="Extra keyword term (repeatable).",
    )
    parser.add_argument(
        "--developer-prompt-file",
        default=str(default_prompt_template),
        help="Path to developer prompt template file.",
    )
    parser.add_argument(
        "--user-task-file",
        default="",
        help="Optional path to user task template file.",
    )
    parser.add_argument(
        "--ad-hoc-requirements",
        default="",
        help="Inline additional requirements appended to prompts.",
    )
    parser.add_argument(
        "--ad-hoc-requirements-file",
        default="",
        help="Optional file with additional requirements appended to prompts.",
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
        "--search-context-size",
        choices=("low", "medium", "high"),
        default="high",
        help="web_search context size (default: high).",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=10.0,
        help="Polling interval seconds (default: 10).",
    )
    parser.add_argument(
        "--heartbeat-seconds",
        type=int,
        default=120,
        help="Quiet-mode heartbeat interval for polling logs (default: 120).",
    )
    parser.add_argument(
        "--max-wait-seconds",
        type=int,
        default=3600,
        help="Maximum wait for completion, 0 disables timeout (default: 3600).",
    )
    parser.add_argument(
        "--max-messages-per-thread",
        type=int,
        default=0,
        help="Limit messages saved per direct thread, 0 keeps all.",
    )
    parser.add_argument(
        "--verbose-poll",
        action="store_true",
        help="Print every polling attempt (default is quiet polling).",
    )
    parser.add_argument(
        "--assemble-only",
        action="store_true",
        help="Assemble dataset and prompts only; do not call the API.",
    )
    return parser


def main() -> int:
    _configure_line_buffering()
    parser = build_parser()
    args = parser.parse_args()

    if args.poll_seconds <= 0:
        parser.error("--poll-seconds must be greater than 0.")
    if args.max_wait_seconds < 0:
        parser.error("--max-wait-seconds must be >= 0.")
    if args.heartbeat_seconds < 0:
        parser.error("--heartbeat-seconds must be >= 0.")
    if args.max_messages_per_thread < 0:
        parser.error("--max-messages-per-thread must be >= 0.")

    load_dotenv()
    if not args.assemble_only and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Add it to environment or .env file.")

    topic = args.topic.strip()
    if not topic:
        raise SystemExit("--topic cannot be empty.")

    sites_root = Path(args.sites_root).expanduser()
    output_root = Path(args.output_root).expanduser()

    archives = discover_archives(sites_root)
    selected_archives = select_archives(archives, args.archive_scope)
    status_line(
        f"selected_archives scope={args.archive_scope} count={len(selected_archives)} "
        f"names={[a.path.name for a in selected_archives]}"
    )

    keyword_pattern, keyword_terms, keyword_pattern_raw = build_keyword_regex(
        topic=topic,
        keyword_regex=args.keyword_regex,
        extra_keywords=args.keyword,
    )
    status_line(f"keyword_pattern={keyword_pattern_raw}")

    assembled = assemble_topic_dataset(
        selected_archives=selected_archives,
        topic=topic,
        keyword_pattern=keyword_pattern,
        keyword_pattern_raw=keyword_pattern_raw,
        keyword_terms=keyword_terms,
        scope=args.archive_scope,
        max_messages_per_thread=args.max_messages_per_thread,
    )

    matched = int(assembled["summary"]["matched_conversation_ids"])
    direct = int(assembled["summary"]["direct_topic_threads"])
    incidental = int(assembled["summary"]["incidental_mentions"])
    status_line(f"assembled_dataset matched={matched} direct={direct} incidental={incidental}")
    if matched == 0:
        raise SystemExit("No matching conversations found for topic/keyword pattern.")

    ad_hoc_file = (
        Path(args.ad_hoc_requirements_file).expanduser()
        if args.ad_hoc_requirements_file.strip()
        else None
    )
    ad_hoc_requirements = _combine_ad_hoc_requirements(args.ad_hoc_requirements, ad_hoc_file)

    developer_prompt = _load_developer_prompt(
        template_path=Path(args.developer_prompt_file).expanduser(),
        topic=topic,
        ad_hoc_requirements=ad_hoc_requirements,
    )
    user_task_file = (
        Path(args.user_task_file).expanduser() if args.user_task_file.strip() else None
    )
    user_task = _load_user_task(user_task_file, topic=topic, ad_hoc_requirements=ad_hoc_requirements)

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / f"{timestamp}_{slugify(topic)[:64]}"
    run_dir.mkdir(parents=True, exist_ok=True)

    assembled_path = run_dir / "assembled_dataset.json"
    dev_prompt_path = run_dir / "developer_prompt_effective.txt"
    user_task_path = run_dir / "user_task_effective.txt"
    report_path = run_dir / "report.md"
    response_path = run_dir / "response_payload.json"
    manifest_path = run_dir / "run_manifest.json"

    assembled_path.write_text(json.dumps(assembled, indent=2, ensure_ascii=False), encoding="utf-8")
    dev_prompt_path.write_text(developer_prompt, encoding="utf-8")
    user_task_path.write_text(user_task, encoding="utf-8")

    manifest: dict[str, Any] = {
        "created_at_utc": utc_now_iso(),
        "topic": topic,
        "archive_scope": args.archive_scope,
        "selected_archives": [a.path.name for a in selected_archives],
        "keyword_regex": keyword_pattern_raw,
        "keyword_terms": keyword_terms,
        "summary": assembled.get("summary"),
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "verbosity": args.verbosity,
        "search_context_size": args.search_context_size,
        "artifacts": {
            "assembled_dataset_json": str(assembled_path),
            "developer_prompt_effective_txt": str(dev_prompt_path),
            "user_task_effective_txt": str(user_task_path),
            "report_md": str(report_path),
            "response_payload_json": str(response_path),
        },
    }

    if args.assemble_only:
        manifest["status"] = "assembled_only"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        status_line(f"assemble_only=true run_dir={run_dir}")
        status_line(f"assembled_json={assembled_path}")
        status_line(f"manifest={manifest_path}")
        return 0

    dataset_json = json.dumps(assembled, indent=2, ensure_ascii=False)
    user_content = (
        f"{user_task}\n\n"
        "Input JSON:\n"
        "```json\n"
        f"{dataset_json}\n"
        "```"
    )
    messages = [
        {"role": "developer", "content": [{"type": "input_text", "text": developer_prompt}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_content}]},
    ]

    status_line(f"submitting_background_request model={args.model} run_dir={run_dir}")
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
        raise SystemExit("API request did not return a response id.")

    status_line(f"submitted response_id={response_id} initial_status={getattr(created, 'status', 'unknown')}")
    final_response = poll_background(
        client=client,
        response_id=response_id,
        poll_seconds=args.poll_seconds,
        max_wait_seconds=args.max_wait_seconds,
        heartbeat_seconds=args.heartbeat_seconds,
        verbose_poll=args.verbose_poll,
    )

    final_status = getattr(final_response, "status", "unknown")
    report_text = _extract_output_text(final_response)

    response_path.write_text(
        json.dumps(_to_plain_json(final_response), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    report_path.write_text(report_text, encoding="utf-8")

    manifest["response_id"] = response_id
    manifest["status"] = final_status
    manifest["completed_at_utc"] = utc_now_iso()
    manifest["report_chars"] = len(report_text)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    status_line(f"final_status={final_status} response_id={response_id}")
    status_line(f"report={report_path}")
    status_line(f"response_json={response_path}")
    status_line(f"manifest={manifest_path}")

    return 0 if final_status == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
