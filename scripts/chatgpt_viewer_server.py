#!/usr/bin/env python3
"""Local server for ChatGPT archive viewer with live chat authoring support."""

import argparse
import json
import os
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from flask import Flask, jsonify, request, send_from_directory
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: flask. Install requirements before running this server."
    ) from exc

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: openai. Install requirements before running this server."
    ) from exc

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*args, **kwargs):
        return False


VALID_REASONING = {"none", "low", "medium", "high", "xhigh"}
VALID_VERBOSITY = {"low", "medium", "high"}
MAX_CONVERSATION_TITLE_CHARS = 80


def default_web_search_tool() -> Dict[str, object]:
    return {
        "type": "web_search",
        "user_location": {"type": "approximate"},
        "search_context_size": "high",
    }


def now_ts() -> float:
    return time.time()


def atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, separators=(",", ":"))
    tmp_path.replace(path)


def make_message_node(
    node_id: str,
    role: str,
    text: str,
    parent_id: Optional[str],
    created_at: float,
    *,
    model: Optional[str] = None,
) -> Dict[str, object]:
    metadata: Dict[str, object] = {"can_save": True}
    if role == "assistant" and model:
        metadata["model_slug"] = model
        metadata["default_model_slug"] = model

    message = {
        "id": node_id,
        "author": {"role": role, "name": None, "metadata": {}},
        "create_time": created_at,
        "update_time": None,
        "content": {"content_type": "text", "parts": [text]},
        "status": "finished_successfully",
        "end_turn": True if role == "assistant" else None,
        "weight": 1.0,
        "metadata": metadata,
        "recipient": "all",
        "channel": None,
    }
    return {
        "id": node_id,
        "message": message,
        "parent": parent_id,
        "children": [],
    }


def normalize_choice(value: object, allowed: set, default: str) -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"Expected one of {sorted(allowed)}.")
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"Expected one of {sorted(allowed)}.")
    return normalized


def normalize_prompt(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("prompt must be a string.")
    text = value.strip()
    if not text:
        raise ValueError("prompt must not be empty.")
    return text


def normalize_optional_title(value: object) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("title must be a string.")
    text = " ".join(value.strip().split())
    if not text:
        return None
    if len(text) > MAX_CONVERSATION_TITLE_CHARS:
        raise ValueError(
            f"title must be {MAX_CONVERSATION_TITLE_CHARS} characters or fewer."
        )
    return text


def parse_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    raise ValueError("background must be a boolean.")


def extract_message_text(message: Dict[str, object]) -> str:
    content = message.get("content")
    if not isinstance(content, dict):
        return ""

    content_type = content.get("content_type")
    parts: List[str] = []

    if content_type in {"text", "multimodal_text"}:
        raw_parts = content.get("parts")
        if isinstance(raw_parts, list):
            for part in raw_parts:
                if isinstance(part, str):
                    text = part.strip()
                    if text:
                        parts.append(text)
                elif isinstance(part, dict):
                    text = part.get("text")
                    if isinstance(text, str) and text.strip():
                        parts.append(text.strip())
        fallback_text = content.get("text")
        if not parts and isinstance(fallback_text, str) and fallback_text.strip():
            parts.append(fallback_text.strip())
    elif content_type == "code":
        text = content.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())
    elif content_type == "execution_output":
        text = content.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())

    return "\n\n".join(parts).strip()


def normalize_turns(turns: List[Dict[str, str]]) -> List[Dict[str, str]]:
    filtered = [
        {"role": t["role"], "text": t["text"].strip()}
        for t in turns
        if t.get("role") in {"user", "assistant"} and isinstance(t.get("text"), str) and t["text"].strip()
    ]

    while filtered and filtered[0]["role"] != "user":
        filtered.pop(0)

    collapsed: List[Dict[str, str]] = []
    for turn in filtered:
        if not collapsed:
            collapsed.append(turn)
            continue
        if collapsed[-1]["role"] == turn["role"]:
            collapsed[-1] = turn
        else:
            collapsed.append(turn)

    while collapsed and collapsed[0]["role"] != "user":
        collapsed.pop(0)

    return collapsed


def build_api_messages_from_turns(turns: List[Dict[str, str]], prompt: str) -> List[Dict[str, object]]:
    normalized = normalize_turns(turns)

    # Ensure history ends at assistant so appending a new user keeps strict alternation.
    while normalized and normalized[-1]["role"] == "user":
        normalized.pop()

    normalized.append({"role": "user", "text": prompt})

    if not normalized or normalized[0]["role"] != "user" or normalized[-1]["role"] != "user":
        raise ValueError("Conversation input must start and end with user.")

    for idx in range(1, len(normalized)):
        if normalized[idx]["role"] == normalized[idx - 1]["role"]:
            raise ValueError("Conversation input must alternate user and assistant.")

    messages: List[Dict[str, object]] = []
    for turn in normalized:
        if turn["role"] == "user":
            block_type = "input_text"
        else:
            block_type = "output_text"
        messages.append(
            {
                "role": turn["role"],
                "content": [{"type": block_type, "text": turn["text"]}],
            }
        )
    return messages


def extract_output_text(response) -> str:
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) != "message":
            continue
        for block in getattr(item, "content", []) or []:
            if getattr(block, "type", None) != "output_text":
                continue
            text = getattr(block, "text", "")
            if isinstance(text, str) and text.strip():
                chunks.append(text.strip())
    return "\n\n".join(chunks).strip()


class ArchiveStore:
    def __init__(self, viewer_dir: Path):
        self.viewer_dir = viewer_dir
        self.data_dir = viewer_dir / "viewer_data"
        self.index_path = self.data_dir / "index.json"
        self.conv_dir = self.data_dir / "conversations"
        self.lock = threading.Lock()

    def require_ready(self) -> None:
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Missing data directory: {self.data_dir}")
        if not self.conv_dir.exists():
            raise FileNotFoundError(f"Missing conversation directory: {self.conv_dir}")
        if not self.index_path.exists():
            atomic_write_json(self.index_path, [])

    def load_index(self) -> List[Dict[str, object]]:
        if not self.index_path.exists():
            return []
        with self.index_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, list):
            return []
        return payload

    def save_index(self, index: List[Dict[str, object]]) -> None:
        atomic_write_json(self.index_path, index)

    def conv_path(self, conv_id: str) -> Path:
        return self.conv_dir / f"{conv_id}.json"

    def load_conversation(self, conv_id: str) -> Dict[str, object]:
        path = self.conv_path(conv_id)
        if not path.exists():
            raise FileNotFoundError(f"Conversation not found: {conv_id}")
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError(f"Invalid conversation JSON for {conv_id}")
        return payload

    def save_conversation(self, conv: Dict[str, object]) -> None:
        conv_id = conv.get("id")
        if not isinstance(conv_id, str) or not conv_id:
            raise ValueError("Conversation id is missing.")
        atomic_write_json(self.conv_path(conv_id), conv)

    @staticmethod
    def to_index_entry(conv: Dict[str, object]) -> Dict[str, object]:
        mapping = conv.get("mapping")
        if not isinstance(mapping, dict):
            mapping = {}
        node_count = len(mapping)
        message_count = sum(1 for node in mapping.values() if isinstance(node, dict) and node.get("message"))
        return {
            "id": conv.get("id"),
            "title": conv.get("title") or "(untitled)",
            "create_time": conv.get("create_time"),
            "update_time": conv.get("update_time"),
            "current_node": conv.get("current_node"),
            "node_count": node_count,
            "message_count": message_count,
        }

    def upsert_index_entry(self, entry: Dict[str, object]) -> List[Dict[str, object]]:
        index = self.load_index()
        replaced = False
        for idx, row in enumerate(index):
            if isinstance(row, dict) and row.get("id") == entry.get("id"):
                index[idx] = entry
                replaced = True
                break
        if not replaced:
            index.append(entry)
        index.sort(key=lambda item: item.get("update_time") or 0, reverse=True)
        self.save_index(index)
        return index


class ChatService:
    def __init__(self, store: ArchiveStore):
        self.store = store
        self._client: Optional[OpenAI] = None
        self.pending_background: Dict[str, Dict[str, object]] = {}

    def get_client(self) -> OpenAI:
        if self._client is not None:
            return self._client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set in environment.")
        self._client = OpenAI(api_key=api_key)
        return self._client

    def call_model(
        self,
        messages: List[Dict[str, object]],
        *,
        model: str,
        reasoning_effort: str,
        text_verbosity: str,
        background: bool,
    ):
        payload: Dict[str, object] = {
            "model": model,
            "input": messages,
            "text": {"format": {"type": "text"}, "verbosity": text_verbosity},
            "reasoning": {"summary": None, "effort": reasoning_effort},
            "tools": [default_web_search_tool()],
        }
        if background:
            payload["background"] = True
        else:
            payload["store"] = True
        client = self.get_client()
        return client.responses.create(**payload)

    def build_turns_from_path(self, conv: Dict[str, object], anchor_node_id: str) -> List[Dict[str, str]]:
        mapping = conv.get("mapping")
        if not isinstance(mapping, dict):
            raise ValueError("Conversation mapping is invalid.")
        if anchor_node_id not in mapping:
            raise ValueError("anchor_node_id does not exist in conversation.")

        path: List[str] = []
        current = anchor_node_id
        while current and current in mapping:
            path.append(current)
            parent = mapping[current].get("parent")
            current = parent if isinstance(parent, str) else None
        path.reverse()

        turns: List[Dict[str, str]] = []
        for node_id in path:
            node = mapping.get(node_id)
            if not isinstance(node, dict):
                continue
            msg = node.get("message")
            if not isinstance(msg, dict):
                continue
            author = msg.get("author")
            role = author.get("role") if isinstance(author, dict) else None
            if role not in {"user", "assistant"}:
                continue
            text = extract_message_text(msg)
            if text:
                turns.append({"role": role, "text": text})
        return turns

    def persist_new_conversation(
        self,
        prompt: str,
        assistant_text: str,
        *,
        model: str,
        title: str,
    ) -> Tuple[Dict[str, object], Dict[str, object], str]:
        timestamp = now_ts()
        conv_id = str(uuid.uuid4())
        root_id = "client-created-root"
        user_id = str(uuid.uuid4())
        assistant_id = str(uuid.uuid4())

        mapping: Dict[str, object] = {
            root_id: {
                "id": root_id,
                "message": None,
                "parent": None,
                "children": [user_id],
            },
            user_id: make_message_node(user_id, "user", prompt, root_id, timestamp),
            assistant_id: make_message_node(
                assistant_id,
                "assistant",
                assistant_text,
                user_id,
                timestamp,
                model=model,
            ),
        }
        mapping[user_id]["children"] = [assistant_id]

        conv = {
            "id": conv_id,
            "title": title or "(untitled)",
            "create_time": timestamp,
            "update_time": timestamp,
            "current_node": assistant_id,
            "mapping": mapping,
        }

        with self.store.lock:
            self.store.save_conversation(conv)
            index_entry = self.store.to_index_entry(conv)
            self.store.upsert_index_entry(index_entry)
        return conv, index_entry, assistant_id

    def persist_continuation(
        self,
        conv_id: str,
        anchor_node_id: str,
        prompt: str,
        assistant_text: str,
        *,
        model: str,
    ) -> Tuple[Dict[str, object], Dict[str, object], str]:
        with self.store.lock:
            conv = self.store.load_conversation(conv_id)
            mapping = conv.get("mapping")
            if not isinstance(mapping, dict):
                raise ValueError("Conversation mapping is invalid.")
            if anchor_node_id not in mapping:
                raise ValueError("anchor_node_id does not exist in conversation.")

            timestamp = now_ts()
            user_id = str(uuid.uuid4())
            assistant_id = str(uuid.uuid4())

            anchor_node = mapping.get(anchor_node_id)
            children = anchor_node.get("children")
            if not isinstance(children, list):
                children = []
                anchor_node["children"] = children
            children.append(user_id)

            mapping[user_id] = make_message_node(user_id, "user", prompt, anchor_node_id, timestamp)
            mapping[assistant_id] = make_message_node(
                assistant_id,
                "assistant",
                assistant_text,
                user_id,
                timestamp,
                model=model,
            )
            mapping[user_id]["children"] = [assistant_id]

            conv["current_node"] = assistant_id
            conv["update_time"] = timestamp

            self.store.save_conversation(conv)
            index_entry = self.store.to_index_entry(conv)
            self.store.upsert_index_entry(index_entry)
        return conv, index_entry, assistant_id

    def start_background_job(self, response_id: str, payload: Dict[str, object]) -> None:
        with self.store.lock:
            self.pending_background[response_id] = payload

    def get_background_job(self, response_id: str) -> Optional[Dict[str, object]]:
        with self.store.lock:
            return self.pending_background.get(response_id)

    def set_background_job(self, response_id: str, payload: Dict[str, object]) -> None:
        with self.store.lock:
            self.pending_background[response_id] = payload


def title_from_prompt(prompt: str) -> str:
    text = " ".join(prompt.strip().split())
    if not text:
        return "(untitled)"
    if len(text) <= MAX_CONVERSATION_TITLE_CHARS:
        return text
    return text[: MAX_CONVERSATION_TITLE_CHARS - 3].rstrip() + "..."


def make_app(viewer_dir: Path) -> Flask:
    load_dotenv()

    app = Flask(__name__, static_folder=None)
    store = ArchiveStore(viewer_dir)
    store.require_ready()
    chat = ChatService(store)

    @app.get("/api/archive/health")
    def archive_health():
        return jsonify(ok=True, viewer_dir=str(viewer_dir))

    @app.post("/api/archive/chat/new")
    def create_new_conversation():
        payload = request.get_json(silent=True) or {}

        try:
            prompt = normalize_prompt(payload.get("prompt"))
            custom_title = normalize_optional_title(payload.get("title"))
            model = payload.get("model") if isinstance(payload.get("model"), str) else "gpt-5.1"
            model = model.strip() or "gpt-5.1"
            reasoning_effort = normalize_choice(
                payload.get("reasoning_effort"), VALID_REASONING, "high"
            )
            text_verbosity = normalize_choice(
                payload.get("text_verbosity"), VALID_VERBOSITY, "medium"
            )
            background = parse_bool(payload.get("background"), False)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400

        conv_title = custom_title or title_from_prompt(prompt)
        messages = build_api_messages_from_turns([], prompt)

        try:
            response = chat.call_model(
                messages,
                model=model,
                reasoning_effort=reasoning_effort,
                text_verbosity=text_verbosity,
                background=background,
            )
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to create model response for new conversation")
            return jsonify(ok=False, error=str(exc)), 500

        if background:
            response_id = getattr(response, "id", None)
            if not isinstance(response_id, str) or not response_id:
                return jsonify(ok=False, error="No response_id returned for background request."), 500
            chat.start_background_job(
                response_id,
                {
                    "mode": "new",
                    "prompt": prompt,
                    "model": model,
                    "title": conv_title,
                    "persisted": False,
                },
            )
            return jsonify(
                ok=True,
                background=True,
                response_id=response_id,
                status=getattr(response, "status", "queued"),
                done=False,
            )

        assistant_text = extract_output_text(response)
        try:
            conv, index_entry, selected_node_id = chat.persist_new_conversation(
                prompt,
                assistant_text,
                model=model,
                title=conv_title,
            )
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to persist new conversation")
            return jsonify(ok=False, error=str(exc)), 500

        return jsonify(
            ok=True,
            background=False,
            done=True,
            conversation=conv,
            index_entry=index_entry,
            selected_node_id=selected_node_id,
            output_text=assistant_text,
        )

    @app.post("/api/archive/chat/continue")
    def continue_conversation():
        payload = request.get_json(silent=True) or {}

        try:
            conv_id = payload.get("conversation_id")
            anchor_node_id = payload.get("anchor_node_id")
            if not isinstance(conv_id, str) or not conv_id.strip():
                raise ValueError("conversation_id is required.")
            if not isinstance(anchor_node_id, str) or not anchor_node_id.strip():
                raise ValueError("anchor_node_id is required.")
            conv_id = conv_id.strip()
            anchor_node_id = anchor_node_id.strip()

            prompt = normalize_prompt(payload.get("prompt"))
            model = payload.get("model") if isinstance(payload.get("model"), str) else "gpt-5.1"
            model = model.strip() or "gpt-5.1"
            reasoning_effort = normalize_choice(
                payload.get("reasoning_effort"), VALID_REASONING, "high"
            )
            text_verbosity = normalize_choice(
                payload.get("text_verbosity"), VALID_VERBOSITY, "medium"
            )
            background = parse_bool(payload.get("background"), False)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400

        try:
            conv = store.load_conversation(conv_id)
            turns = chat.build_turns_from_path(conv, anchor_node_id)
            messages = build_api_messages_from_turns(turns, prompt)
        except FileNotFoundError as exc:
            return jsonify(ok=False, error=str(exc)), 404
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to prepare continuation context")
            return jsonify(ok=False, error=str(exc)), 500

        try:
            response = chat.call_model(
                messages,
                model=model,
                reasoning_effort=reasoning_effort,
                text_verbosity=text_verbosity,
                background=background,
            )
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to create model response for continuation")
            return jsonify(ok=False, error=str(exc)), 500

        if background:
            response_id = getattr(response, "id", None)
            if not isinstance(response_id, str) or not response_id:
                return jsonify(ok=False, error="No response_id returned for background request."), 500
            chat.start_background_job(
                response_id,
                {
                    "mode": "continue",
                    "conversation_id": conv_id,
                    "anchor_node_id": anchor_node_id,
                    "prompt": prompt,
                    "model": model,
                    "persisted": False,
                },
            )
            return jsonify(
                ok=True,
                background=True,
                response_id=response_id,
                status=getattr(response, "status", "queued"),
                done=False,
            )

        assistant_text = extract_output_text(response)
        try:
            conv, index_entry, selected_node_id = chat.persist_continuation(
                conv_id,
                anchor_node_id,
                prompt,
                assistant_text,
                model=model,
            )
        except FileNotFoundError as exc:
            return jsonify(ok=False, error=str(exc)), 404
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to persist continuation")
            return jsonify(ok=False, error=str(exc)), 500

        return jsonify(
            ok=True,
            background=False,
            done=True,
            conversation=conv,
            index_entry=index_entry,
            selected_node_id=selected_node_id,
            output_text=assistant_text,
        )

    @app.get("/api/archive/chat/background/<response_id>")
    def poll_background(response_id: str):
        if not response_id:
            return jsonify(ok=False, error="response_id is required."), 400

        job = chat.get_background_job(response_id)
        if job is None:
            return jsonify(ok=False, error="Unknown background response_id."), 404

        try:
            response = chat.get_client().responses.retrieve(response_id)
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Background poll failed")
            return jsonify(ok=False, error=str(exc)), 500

        status = getattr(response, "status", "")
        done = status in {"completed", "failed", "cancelled"}

        if done and status == "completed":
            persisted = bool(job.get("persisted"))
            if not persisted:
                assistant_text = extract_output_text(response)
                try:
                    if job.get("mode") == "new":
                        conv, index_entry, selected_node_id = chat.persist_new_conversation(
                            job.get("prompt", ""),
                            assistant_text,
                            model=job.get("model", "gpt-5.1"),
                            title=job.get("title", "(untitled)"),
                        )
                    else:
                        conv, index_entry, selected_node_id = chat.persist_continuation(
                            job.get("conversation_id", ""),
                            job.get("anchor_node_id", ""),
                            job.get("prompt", ""),
                            assistant_text,
                            model=job.get("model", "gpt-5.1"),
                        )
                    job["persisted"] = True
                    job["result"] = {
                        "conversation": conv,
                        "index_entry": index_entry,
                        "selected_node_id": selected_node_id,
                        "output_text": assistant_text,
                    }
                    chat.set_background_job(response_id, job)
                except Exception as exc:  # noqa: BLE001
                    app.logger.exception("Failed to persist completed background job")
                    return jsonify(ok=False, error=str(exc), status=status, done=True), 500

            result = job.get("result") or {}
            return jsonify(
                ok=True,
                status=status,
                done=True,
                conversation=result.get("conversation"),
                index_entry=result.get("index_entry"),
                selected_node_id=result.get("selected_node_id"),
                output_text=result.get("output_text", ""),
            )

        payload = {
            "ok": True,
            "status": status,
            "done": done,
            "output_text": extract_output_text(response) if done and status == "completed" else "",
        }
        return jsonify(payload)

    @app.post("/api/archive/chat/background/<response_id>/cancel")
    def cancel_background(response_id: str):
        if not response_id:
            return jsonify(ok=False, error="response_id is required."), 400
        job = chat.get_background_job(response_id)
        if job is None:
            return jsonify(ok=False, error="Unknown background response_id."), 404
        try:
            response = chat.get_client().responses.cancel(response_id)
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Background cancellation failed")
            return jsonify(ok=False, error=str(exc)), 500
        status = getattr(response, "status", "")
        done = status in {"completed", "failed", "cancelled"}
        return jsonify(ok=True, status=status, done=done)

    @app.get("/")
    def serve_root():
        return send_from_directory(viewer_dir, "viewer.html")

    @app.get("/<path:asset_path>")
    def serve_static(asset_path: str):
        if asset_path.startswith("api/"):
            return jsonify(ok=False, error="Not found."), 404
        return send_from_directory(viewer_dir, asset_path)

    return app


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Serve a ChatGPT viewer site with live chat authoring support."
    )
    parser.add_argument(
        "--viewer-dir",
        "-d",
        required=True,
        help="Path to built viewer site folder (contains viewer.html and viewer_data).",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000).")
    args = parser.parse_args()

    viewer_dir = Path(args.viewer_dir).expanduser().resolve()
    if not viewer_dir.exists():
        raise SystemExit(f"Viewer directory not found: {viewer_dir}")
    if not (viewer_dir / "viewer.html").exists():
        raise SystemExit(f"viewer.html missing in {viewer_dir}")

    app = make_app(viewer_dir)
    app.run(host=args.host, port=args.port, debug=os.getenv("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
