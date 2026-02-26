#!/usr/bin/env python3
"""Local server for ChatGPT archive viewer with single-archive and hub modes."""

import argparse
import copy
import json
import os
import re
import shutil
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

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

try:
    from viewer_asset_utils import ASSET_ARCHIVE_DIR, copy_archive_to
except ImportError:  # pragma: no cover
    from scripts.viewer_asset_utils import ASSET_ARCHIVE_DIR, copy_archive_to


VALID_REASONING = {"none", "low", "medium", "high", "xhigh"}
VALID_VERBOSITY = {"low", "medium", "high"}
MAX_CONVERSATION_TITLE_CHARS = 80
MAX_ARCHIVE_INPUT_CHARS = 80
ARCHIVE_DIR_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".heif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}
TERMINAL_RESPONSE_STATUSES = {
    "cancelled",
    "completed",
    "expired",
    "failed",
    "incomplete",
}


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


def is_gpt4_family_model(model: str) -> bool:
    normalized = model.strip().lower()
    return normalized.startswith("gpt-4") or normalized.startswith("gpt4")


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


def normalize_optional_archive_input(value: object, field_name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")
    text = " ".join(value.strip().split())
    if not text:
        return None
    if len(text) > MAX_ARCHIVE_INPUT_CHARS:
        raise ValueError(f"{field_name} must be {MAX_ARCHIVE_INPUT_CHARS} characters or fewer.")
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


def sanitize_attachment_filename(value: object) -> str:
    if not isinstance(value, str):
        return ""
    text = value.strip().replace("\\", "/")
    if not text:
        return ""
    text = text.split("/")[-1].strip()
    return text


def attachment_is_image(filename: str, content_type: str) -> bool:
    if isinstance(content_type, str) and content_type.strip().lower().startswith("image/"):
        return True
    suffix = Path(filename).suffix.lower()
    return suffix in IMAGE_EXTENSIONS


def normalize_request_attachments(files: List[object]) -> List[Dict[str, object]]:
    normalized: List[Dict[str, object]] = []
    for raw_file in files:
        filename = sanitize_attachment_filename(getattr(raw_file, "filename", ""))
        if not filename:
            continue
        content_type = getattr(raw_file, "mimetype", None) or getattr(raw_file, "content_type", None)
        if not isinstance(content_type, str):
            content_type = "application/octet-stream"
        content_type = content_type.strip().lower() or "application/octet-stream"

        is_image = attachment_is_image(filename, content_type)
        normalized.append(
            {
                "file": raw_file,
                "filename": filename,
                "content_type": content_type,
                "purpose": "vision" if is_image else "user_data",
                "api_content_type": "input_image" if is_image else "input_file",
            }
        )
    return normalized


def parse_chat_request_payload(http_request) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    content_type = (http_request.content_type or "").lower()
    if "multipart/form-data" in content_type:
        raw_payload = http_request.form.get("payload_json")
        if raw_payload is None:
            raise ValueError("payload_json is required for multipart requests.")
        try:
            payload = json.loads(raw_payload)
        except json.JSONDecodeError as exc:
            raise ValueError("payload_json must be valid JSON.") from exc
        if not isinstance(payload, dict):
            raise ValueError("payload_json must decode to a JSON object.")
        attachments = normalize_request_attachments(http_request.files.getlist("attachments"))
        return payload, attachments

    payload = http_request.get_json(silent=True)
    if payload is None:
        payload = {}
    if not isinstance(payload, dict):
        raise ValueError("JSON body must be an object.")
    return payload, []


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
        if t.get("role") in {"user", "assistant"}
        and isinstance(t.get("text"), str)
        and t["text"].strip()
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


def build_api_messages_from_turns(
    turns: List[Dict[str, str]], prompt: str
) -> List[Dict[str, object]]:
    normalized = normalize_turns(turns)

    # Ensure history ends at assistant so appending a new user keeps strict alternation.
    while normalized and normalized[-1]["role"] == "user":
        normalized.pop()

    normalized.append({"role": "user", "text": prompt})

    if (
        not normalized
        or normalized[0]["role"] != "user"
        or normalized[-1]["role"] != "user"
    ):
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
        message_count = sum(
            1 for node in mapping.values() if isinstance(node, dict) and node.get("message")
        )
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
            "text": {"format": {"type": "text"}},
            "tools": [default_web_search_tool()],
        }
        if is_gpt4_family_model(model):
            payload["temperature"] = 1
            payload["top_p"] = 1
            payload["max_output_tokens"] = 16000
        else:
            payload["text"]["verbosity"] = text_verbosity
            payload["reasoning"] = {"summary": None, "effort": reasoning_effort}
        if background:
            payload["background"] = True
        else:
            payload["store"] = True
        client = self.get_client()
        return client.responses.create(**payload)

    def prepare_messages_with_attachments(
        self,
        messages: List[Dict[str, object]],
        attachments: List[Dict[str, object]],
    ) -> Tuple[List[Dict[str, object]], List[str]]:
        if not attachments:
            return messages, []

        enriched_messages = copy.deepcopy(messages)
        if not enriched_messages:
            raise ValueError("Conversation input is empty.")

        last_message = enriched_messages[-1]
        if not isinstance(last_message, dict) or last_message.get("role") != "user":
            raise ValueError("Conversation input must end with a user message.")

        content = last_message.get("content")
        if not isinstance(content, list):
            raise ValueError("Conversation input is invalid.")
        if not any(isinstance(block, dict) and block.get("type") == "input_text" for block in content):
            raise ValueError("Final user message must include input_text.")

        client = self.get_client()
        uploaded_file_ids: List[str] = []
        try:
            for attachment in attachments:
                file_storage = attachment.get("file")
                stream = getattr(file_storage, "stream", None)
                if stream is None:
                    raise ValueError("Attachment stream is missing.")

                filename = attachment.get("filename")
                if not isinstance(filename, str) or not filename:
                    raise ValueError("Attachment filename is missing.")

                content_type = attachment.get("content_type")
                if not isinstance(content_type, str) or not content_type:
                    content_type = "application/octet-stream"

                purpose = attachment.get("purpose")
                if purpose not in {"vision", "user_data"}:
                    purpose = "user_data"

                try:
                    stream.seek(0)
                except Exception:  # noqa: BLE001
                    pass

                uploaded = client.files.create(
                    file=(filename, stream, content_type),
                    purpose=purpose,
                )
                uploaded_id = getattr(uploaded, "id", None)
                if not isinstance(uploaded_id, str) or not uploaded_id:
                    raise RuntimeError(f"Upload returned no file id for {filename}.")
                uploaded_file_ids.append(uploaded_id)

                api_content_type = attachment.get("api_content_type")
                if api_content_type == "input_image":
                    content.append({"type": "input_image", "image_file_id": uploaded_id})
                else:
                    content.append({"type": "input_file", "file_id": uploaded_id})
        except Exception:
            self.cleanup_uploaded_files(uploaded_file_ids)
            raise
        return enriched_messages, uploaded_file_ids

    def cleanup_uploaded_files(self, uploaded_file_ids: List[str]) -> List[str]:
        if not uploaded_file_ids:
            return []
        client = self.get_client()
        errors: List[str] = []
        seen = set()
        for file_id in uploaded_file_ids:
            if not isinstance(file_id, str) or not file_id or file_id in seen:
                continue
            seen.add(file_id)
            try:
                client.files.delete(file_id)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{file_id}: {exc}")
        return errors

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

            mapping[user_id] = make_message_node(
                user_id,
                "user",
                prompt,
                anchor_node_id,
                timestamp,
            )
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


def slugify_archive_name(raw: str) -> str:
    lowered = raw.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        slug = "blank-archive"
    if len(slug) > 64:
        slug = slug[:64].rstrip("-")
    return slug or "blank-archive"


def validate_archive_dir_name(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("archive id is required.")
    if not ARCHIVE_DIR_NAME_PATTERN.fullmatch(value):
        raise ValueError("archive id is invalid.")
    return value


def archive_title_from_slug(slug: str) -> str:
    title = slug.replace("_", " ").replace("-", " ").strip()
    return title or slug


class ArchiveHub:
    def __init__(
        self,
        sites_root: Path,
        viewer_template_path: Path,
        hub_template_path: Path,
        *,
        asset_archive_dir: Path = ASSET_ARCHIVE_DIR,
    ):
        self.sites_root = sites_root
        self.viewer_template_path = viewer_template_path
        self.hub_template_path = hub_template_path
        self.asset_archive_dir = asset_archive_dir
        self.lock = threading.Lock()
        self._service_cache: Dict[str, Tuple[Path, ArchiveStore, ChatService]] = {}
        self.sites_root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _looks_like_archive_dir(viewer_dir: Path) -> bool:
        data_dir = viewer_dir / "viewer_data"
        return (
            viewer_dir.is_dir()
            and (viewer_dir / "viewer.html").is_file()
            and data_dir.is_dir()
            and (data_dir / "index.json").is_file()
            and (data_dir / "conversations").is_dir()
        )

    def _archive_dir_for_slug(self, slug: str) -> Path:
        safe_slug = validate_archive_dir_name(slug)
        archive_dir = (self.sites_root / safe_slug).resolve()
        if archive_dir.parent != self.sites_root.resolve():
            raise ValueError("archive id resolves outside of sites root.")
        return archive_dir

    def _describe_archive(self, slug: str, archive_dir: Path) -> Dict[str, object]:
        index_path = archive_dir / "viewer_data" / "index.json"
        conversation_count = 0
        max_update = 0.0

        try:
            payload = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                conversation_count = len(payload)
                for row in payload:
                    if not isinstance(row, dict):
                        continue
                    update_time = row.get("update_time")
                    if isinstance(update_time, (int, float)):
                        max_update = max(max_update, float(update_time))
        except Exception:
            conversation_count = 0

        try:
            max_update = max(max_update, archive_dir.stat().st_mtime)
        except OSError:
            pass

        return {
            "slug": slug,
            "title": archive_title_from_slug(slug),
            "conversation_count": conversation_count,
            "updated_at": max_update,
            "is_blank": conversation_count == 0,
        }

    def list_archives(self) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        if not self.sites_root.exists():
            return rows
        for child in self.sites_root.iterdir():
            if not child.is_dir():
                continue
            slug = child.name
            if not ARCHIVE_DIR_NAME_PATTERN.fullmatch(slug):
                continue
            if not self._looks_like_archive_dir(child):
                continue
            rows.append(self._describe_archive(slug, child))
        rows.sort(key=lambda row: (row.get("updated_at") or 0, row.get("slug") or ""), reverse=True)
        return rows

    def _next_unique_slug(self, base_slug: str) -> str:
        slug = base_slug
        counter = 2
        while (self.sites_root / slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def create_blank_archive(self, *, name: Optional[str], slug: Optional[str]) -> Dict[str, object]:
        with self.lock:
            seed = slug or name or "blank-archive"
            base_slug = slugify_archive_name(seed)
            unique_slug = self._next_unique_slug(base_slug)
            archive_dir = self.sites_root / unique_slug

            try:
                archive_dir.mkdir(parents=True, exist_ok=False)
                viewer_html = archive_dir / "viewer.html"
                viewer_html.write_text(
                    self.viewer_template_path.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )

                data_dir = archive_dir / "viewer_data"
                conv_dir = data_dir / "conversations"
                conv_dir.mkdir(parents=True, exist_ok=True)
                atomic_write_json(data_dir / "index.json", [])
                atomic_write_json(data_dir / "assets.json", {})

                copy_archive_to(archive_dir / "viewer_assets", archive_dir=self.asset_archive_dir)
            except Exception:
                shutil.rmtree(archive_dir, ignore_errors=True)
                raise

            self._service_cache.pop(unique_slug, None)
            return self._describe_archive(unique_slug, archive_dir)

    def get_archive(self, slug: str) -> Tuple[Path, ArchiveStore, ChatService]:
        safe_slug = validate_archive_dir_name(slug)
        archive_dir = self._archive_dir_for_slug(safe_slug)
        if not self._looks_like_archive_dir(archive_dir):
            raise FileNotFoundError(f"Archive not found: {safe_slug}")

        with self.lock:
            cached = self._service_cache.get(safe_slug)
            if cached and cached[0] == archive_dir:
                return cached

            store = ArchiveStore(archive_dir)
            store.require_ready()
            service = ChatService(store)
            cached = (archive_dir, store, service)
            self._service_cache[safe_slug] = cached
            return cached


def log_attachment_cleanup_errors(app: Flask, errors: List[str], *, context: str) -> None:
    for item in errors:
        app.logger.warning("%s attachment cleanup failed: %s", context, item)


def cleanup_background_job_attachments(
    app: Flask,
    chat: ChatService,
    response_id: str,
    job: Dict[str, object],
) -> None:
    if bool(job.get("attachments_cleaned")):
        return
    raw_ids = job.get("uploaded_file_ids")
    uploaded_file_ids = [item for item in raw_ids if isinstance(item, str) and item] if isinstance(raw_ids, list) else []
    errors = chat.cleanup_uploaded_files(uploaded_file_ids) if uploaded_file_ids else []
    if errors:
        job["attachment_cleanup_errors"] = errors
        log_attachment_cleanup_errors(app, errors, context=f"Background response {response_id}")
    job["attachments_cleaned"] = True
    chat.set_background_job(response_id, job)


def process_chat_new(
    app: Flask,
    chat: ChatService,
    payload: Dict[str, object],
    attachments: Optional[List[Dict[str, object]]] = None,
) -> Tuple[Dict[str, object], int]:
    attachments = attachments or []
    try:
        prompt = normalize_prompt(payload.get("prompt"))
        custom_title = normalize_optional_title(payload.get("title"))
        model = payload.get("model") if isinstance(payload.get("model"), str) else "gpt-5.1"
        model = model.strip() or "gpt-5.1"
        reasoning_effort = normalize_choice(payload.get("reasoning_effort"), VALID_REASONING, "high")
        text_verbosity = normalize_choice(payload.get("text_verbosity"), VALID_VERBOSITY, "medium")
        background = parse_bool(payload.get("background"), False)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400

    conv_title = custom_title or title_from_prompt(prompt)
    messages = build_api_messages_from_turns([], prompt)
    uploaded_file_ids: List[str] = []

    try:
        request_messages, uploaded_file_ids = chat.prepare_messages_with_attachments(messages, attachments)
        response = chat.call_model(
            request_messages,
            model=model,
            reasoning_effort=reasoning_effort,
            text_verbosity=text_verbosity,
            background=background,
        )
    except Exception as exc:  # noqa: BLE001
        if uploaded_file_ids:
            cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
            if cleanup_errors:
                log_attachment_cleanup_errors(
                    app,
                    cleanup_errors,
                    context="New chat request",
                )
        app.logger.exception("Failed to create model response for new conversation")
        return {"ok": False, "error": str(exc)}, 500

    if background:
        response_id = getattr(response, "id", None)
        if not isinstance(response_id, str) or not response_id:
            cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
            if cleanup_errors:
                log_attachment_cleanup_errors(
                    app,
                    cleanup_errors,
                    context="New background chat request",
                )
            return {"ok": False, "error": "No response_id returned for background request."}, 500
        chat.start_background_job(
            response_id,
            {
                "mode": "new",
                "prompt": prompt,
                "model": model,
                "title": conv_title,
                "persisted": False,
                "uploaded_file_ids": uploaded_file_ids,
                "attachments_cleaned": False,
            },
        )
        return {
            "ok": True,
            "background": True,
            "response_id": response_id,
            "status": getattr(response, "status", "queued"),
            "done": False,
        }, 200

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
        return {"ok": False, "error": str(exc)}, 500
    finally:
        cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
        if cleanup_errors:
            log_attachment_cleanup_errors(app, cleanup_errors, context="New chat request")

    return {
        "ok": True,
        "background": False,
        "done": True,
        "conversation": conv,
        "index_entry": index_entry,
        "selected_node_id": selected_node_id,
        "output_text": assistant_text,
    }, 200


def process_chat_continue(
    app: Flask,
    store: ArchiveStore,
    chat: ChatService,
    payload: Dict[str, object],
    attachments: Optional[List[Dict[str, object]]] = None,
) -> Tuple[Dict[str, object], int]:
    attachments = attachments or []
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
        reasoning_effort = normalize_choice(payload.get("reasoning_effort"), VALID_REASONING, "high")
        text_verbosity = normalize_choice(payload.get("text_verbosity"), VALID_VERBOSITY, "medium")
        background = parse_bool(payload.get("background"), False)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400

    try:
        conv = store.load_conversation(conv_id)
        turns = chat.build_turns_from_path(conv, anchor_node_id)
        messages = build_api_messages_from_turns(turns, prompt)
    except FileNotFoundError as exc:
        return {"ok": False, "error": str(exc)}, 404
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Failed to prepare continuation context")
        return {"ok": False, "error": str(exc)}, 500

    uploaded_file_ids: List[str] = []
    try:
        request_messages, uploaded_file_ids = chat.prepare_messages_with_attachments(messages, attachments)
        response = chat.call_model(
            request_messages,
            model=model,
            reasoning_effort=reasoning_effort,
            text_verbosity=text_verbosity,
            background=background,
        )
    except Exception as exc:  # noqa: BLE001
        if uploaded_file_ids:
            cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
            if cleanup_errors:
                log_attachment_cleanup_errors(
                    app,
                    cleanup_errors,
                    context="Continue chat request",
                )
        app.logger.exception("Failed to create model response for continuation")
        return {"ok": False, "error": str(exc)}, 500

    if background:
        response_id = getattr(response, "id", None)
        if not isinstance(response_id, str) or not response_id:
            cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
            if cleanup_errors:
                log_attachment_cleanup_errors(
                    app,
                    cleanup_errors,
                    context="Continue background chat request",
                )
            return {"ok": False, "error": "No response_id returned for background request."}, 500
        chat.start_background_job(
            response_id,
            {
                "mode": "continue",
                "conversation_id": conv_id,
                "anchor_node_id": anchor_node_id,
                "prompt": prompt,
                "model": model,
                "persisted": False,
                "uploaded_file_ids": uploaded_file_ids,
                "attachments_cleaned": False,
            },
        )
        return {
            "ok": True,
            "background": True,
            "response_id": response_id,
            "status": getattr(response, "status", "queued"),
            "done": False,
        }, 200

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
        return {"ok": False, "error": str(exc)}, 404
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}, 400
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Failed to persist continuation")
        return {"ok": False, "error": str(exc)}, 500
    finally:
        cleanup_errors = chat.cleanup_uploaded_files(uploaded_file_ids)
        if cleanup_errors:
            log_attachment_cleanup_errors(app, cleanup_errors, context="Continue chat request")

    return {
        "ok": True,
        "background": False,
        "done": True,
        "conversation": conv,
        "index_entry": index_entry,
        "selected_node_id": selected_node_id,
        "output_text": assistant_text,
    }, 200


def process_background_poll(app: Flask, chat: ChatService, response_id: str) -> Tuple[Dict[str, object], int]:
    if not response_id:
        return {"ok": False, "error": "response_id is required."}, 400

    job = chat.get_background_job(response_id)
    if job is None:
        return {"ok": False, "error": "Unknown background response_id."}, 404

    try:
        response = chat.get_client().responses.retrieve(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background poll failed")
        return {"ok": False, "error": str(exc)}, 500

    status = getattr(response, "status", "")
    done = status in TERMINAL_RESPONSE_STATUSES
    if done:
        cleanup_background_job_attachments(app, chat, response_id, job)

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
                return {"ok": False, "error": str(exc), "status": status, "done": True}, 500

        result = job.get("result") or {}
        return {
            "ok": True,
            "status": status,
            "done": True,
            "conversation": result.get("conversation"),
            "index_entry": result.get("index_entry"),
            "selected_node_id": result.get("selected_node_id"),
            "output_text": result.get("output_text", ""),
        }, 200

    return {
        "ok": True,
        "status": status,
        "done": done,
        "output_text": extract_output_text(response) if done and status == "completed" else "",
    }, 200


def process_background_cancel(app: Flask, chat: ChatService, response_id: str) -> Tuple[Dict[str, object], int]:
    if not response_id:
        return {"ok": False, "error": "response_id is required."}, 400
    job = chat.get_background_job(response_id)
    if job is None:
        return {"ok": False, "error": "Unknown background response_id."}, 404
    try:
        response = chat.get_client().responses.cancel(response_id)
    except Exception as exc:  # noqa: BLE001
        app.logger.exception("Background cancellation failed")
        return {"ok": False, "error": str(exc)}, 500
    status = getattr(response, "status", "")
    done = status in TERMINAL_RESPONSE_STATUSES
    if done:
        cleanup_background_job_attachments(app, chat, response_id, job)
    return {"ok": True, "status": status, "done": done}, 200


def make_single_archive_app(viewer_dir: Path) -> Flask:
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
        try:
            payload, attachments = parse_chat_request_payload(request)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        result, status = process_chat_new(app, chat, payload, attachments)
        return jsonify(result), status

    @app.post("/api/archive/chat/continue")
    def continue_conversation():
        try:
            payload, attachments = parse_chat_request_payload(request)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        result, status = process_chat_continue(app, store, chat, payload, attachments)
        return jsonify(result), status

    @app.get("/api/archive/chat/background/<response_id>")
    def poll_background(response_id: str):
        result, status = process_background_poll(app, chat, response_id)
        return jsonify(result), status

    @app.post("/api/archive/chat/background/<response_id>/cancel")
    def cancel_background(response_id: str):
        result, status = process_background_cancel(app, chat, response_id)
        return jsonify(result), status

    @app.get("/")
    def serve_root():
        return send_from_directory(viewer_dir, "viewer.html")

    @app.get("/<path:asset_path>")
    def serve_static(asset_path: str):
        if asset_path.startswith("api/"):
            return jsonify(ok=False, error="Not found."), 404
        return send_from_directory(viewer_dir, asset_path)

    return app


def make_multi_archive_app(sites_root: Path, *, asset_archive_dir: Path = ASSET_ARCHIVE_DIR) -> Flask:
    load_dotenv()

    script_dir = Path(__file__).resolve().parent
    viewer_template_path = script_dir / "chatgpt_viewer_template.html"
    hub_template_path = script_dir / "chatgpt_archive_hub_template.html"
    if not viewer_template_path.exists():
        raise SystemExit(f"viewer template missing: {viewer_template_path}")
    if not hub_template_path.exists():
        raise SystemExit(f"hub template missing: {hub_template_path}")

    hub = ArchiveHub(
        sites_root=sites_root,
        viewer_template_path=viewer_template_path,
        hub_template_path=hub_template_path,
        asset_archive_dir=asset_archive_dir,
    )

    app = Flask(__name__, static_folder=None)

    def resolve_archive_or_response(archive_slug: str):
        try:
            archive_dir, store, chat = hub.get_archive(archive_slug)
        except ValueError as exc:
            return None, jsonify(ok=False, error=str(exc)), 400
        except FileNotFoundError as exc:
            return None, jsonify(ok=False, error=str(exc)), 404
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to resolve archive")
            return None, jsonify(ok=False, error=str(exc)), 500
        return (archive_dir, store, chat), None, None

    @app.get("/")
    def serve_hub_root():
        return send_from_directory(script_dir, hub_template_path.name)

    @app.get("/api/archives")
    def list_archives():
        try:
            archives = hub.list_archives()
            return jsonify(ok=True, archives=archives, sites_root=str(sites_root))
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to list archives")
            return jsonify(ok=False, error=str(exc)), 500

    @app.post("/api/archives")
    def create_archive():
        payload = request.get_json(silent=True) or {}
        try:
            name = normalize_optional_archive_input(payload.get("name"), "name")
            slug = normalize_optional_archive_input(payload.get("slug"), "slug")
            archive = hub.create_blank_archive(name=name, slug=slug)
            open_url = f"/archives/{quote(archive['slug'])}/viewer.html"
            return jsonify(ok=True, archive=archive, open_url=open_url)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        except Exception as exc:  # noqa: BLE001
            app.logger.exception("Failed to create blank archive")
            return jsonify(ok=False, error=str(exc)), 500

    @app.get("/archives/<archive_slug>/")
    def serve_archive_root(archive_slug: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        archive_dir, _, _ = ctx
        return send_from_directory(archive_dir, "viewer.html")

    @app.get("/archives/<archive_slug>/viewer.html")
    def serve_archive_viewer(archive_slug: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        archive_dir, _, _ = ctx
        return send_from_directory(archive_dir, "viewer.html")

    @app.get("/archives/<archive_slug>/<path:asset_path>")
    def serve_archive_assets(archive_slug: str, asset_path: str):
        if asset_path.startswith("api/"):
            return jsonify(ok=False, error="Not found."), 404
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        archive_dir, _, _ = ctx
        return send_from_directory(archive_dir, asset_path)

    @app.get("/api/archives/<archive_slug>/health")
    def archive_health(archive_slug: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        archive_dir, _, _ = ctx
        return jsonify(ok=True, viewer_dir=str(archive_dir), archive_slug=archive_slug)

    @app.post("/api/archives/<archive_slug>/chat/new")
    def archive_chat_new(archive_slug: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        _, _, chat = ctx
        try:
            payload, attachments = parse_chat_request_payload(request)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        result, code = process_chat_new(app, chat, payload, attachments)
        return jsonify(result), code

    @app.post("/api/archives/<archive_slug>/chat/continue")
    def archive_chat_continue(archive_slug: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        _, store, chat = ctx
        try:
            payload, attachments = parse_chat_request_payload(request)
        except ValueError as exc:
            return jsonify(ok=False, error=str(exc)), 400
        result, code = process_chat_continue(app, store, chat, payload, attachments)
        return jsonify(result), code

    @app.get("/api/archives/<archive_slug>/chat/background/<response_id>")
    def archive_chat_background_poll(archive_slug: str, response_id: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        _, _, chat = ctx
        result, code = process_background_poll(app, chat, response_id)
        return jsonify(result), code

    @app.post("/api/archives/<archive_slug>/chat/background/<response_id>/cancel")
    def archive_chat_background_cancel(archive_slug: str, response_id: str):
        ctx, err_resp, status = resolve_archive_or_response(archive_slug)
        if ctx is None:
            return err_resp, status
        _, _, chat = ctx
        result, code = process_background_cancel(app, chat, response_id)
        return jsonify(result), code

    return app


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Serve ChatGPT viewer(s) with live chat authoring support. "
            "Use --viewer-dir for single-archive mode or --sites-root for multi-archive hub mode."
        )
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--viewer-dir",
        "-d",
        help="Path to a single built viewer site folder (contains viewer.html and viewer_data).",
    )
    mode_group.add_argument(
        "--sites-root",
        help=(
            "Path to root folder containing many viewer site folders. "
            "Hub mode serves archive list at /."
        ),
    )
    parser.add_argument(
        "--asset-archive-dir",
        default=str(ASSET_ARCHIVE_DIR),
        help=(
            "Path to canonical offline renderer asset archive for blank archive creation "
            f"(default: {ASSET_ARCHIVE_DIR})."
        ),
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000).")
    args = parser.parse_args()

    if args.viewer_dir:
        viewer_dir = Path(args.viewer_dir).expanduser().resolve()
        if not viewer_dir.exists():
            raise SystemExit(f"Viewer directory not found: {viewer_dir}")
        if not (viewer_dir / "viewer.html").exists():
            raise SystemExit(f"viewer.html missing in {viewer_dir}")
        app = make_single_archive_app(viewer_dir)
    else:
        sites_root = Path(args.sites_root).expanduser().resolve()
        asset_archive_dir = Path(args.asset_archive_dir).expanduser().resolve()
        app = make_multi_archive_app(sites_root, asset_archive_dir=asset_archive_dir)

    app.run(host=args.host, port=args.port, debug=os.getenv("FLASK_DEBUG") == "1")


if __name__ == "__main__":
    main()
