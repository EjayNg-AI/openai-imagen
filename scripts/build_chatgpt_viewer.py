#!/usr/bin/env python3
import argparse
import json
import re
import sys
from json import JSONDecoder
from pathlib import Path


def iter_json_array(path):
    decoder = JSONDecoder()
    with path.open("r", encoding="utf-8") as f:
        buf = ""
        # Seek to first non-whitespace and confirm array start.
        while True:
            chunk = f.read(65536)
            if not chunk:
                return
            buf += chunk
            match = re.search(r"\S", buf)
            if not match:
                continue
            if buf[match.start()] != "[":
                raise ValueError("Expected a JSON array at top-level")
            buf = buf[match.start() + 1 :]
            break

        while True:
            # Skip whitespace and commas between items.
            i = 0
            while i < len(buf) and buf[i] in " \r\n\t,":
                i += 1
            buf = buf[i:]
            if not buf:
                chunk = f.read(65536)
                if not chunk:
                    return
                buf += chunk
                continue
            if buf[0] == "]":
                return
            try:
                obj, idx = decoder.raw_decode(buf)
            except json.JSONDecodeError:
                chunk = f.read(65536)
                if not chunk:
                    return
                buf += chunk
                continue
            yield obj
            buf = buf[idx:]


def extract_assets_json(chat_html_path):
    needle = "var assetsJson = "
    decoder = JSONDecoder()
    with chat_html_path.open("r", encoding="utf-8") as f:
        buf = ""
        while True:
            chunk = f.read(65536)
            if not chunk:
                return {}
            buf += chunk
            idx = buf.find(needle)
            if idx != -1:
                buf = buf[idx + len(needle) :]
                break
            if len(buf) > len(needle):
                buf = buf[-len(needle) :]

        # Skip to first non-whitespace.
        while True:
            match = re.search(r"\S", buf)
            if match:
                buf = buf[match.start() :]
                break
            chunk = f.read(65536)
            if not chunk:
                return {}
            buf += chunk

        if buf.startswith("null"):
            return {}

        # Ensure the buffer starts at a JSON object.
        while buf and buf[0] != "{":
            buf = buf[1:]
        if not buf:
            return {}

        while True:
            try:
                obj, _ = decoder.raw_decode(buf)
                return obj
            except json.JSONDecodeError:
                chunk = f.read(65536)
                if not chunk:
                    raise RuntimeError("Unexpected EOF while parsing assetsJson")
                buf += chunk


def build_viewer(export_dir):
    conv_path = export_dir / "conversations.json"
    chat_path = export_dir / "chat.html"
    if not conv_path.exists():
        raise FileNotFoundError(f"Missing conversations.json in {export_dir}")

    out_dir = export_dir / "viewer_data"
    conv_out_dir = out_dir / "conversations"
    conv_out_dir.mkdir(parents=True, exist_ok=True)

    index = []
    total = 0
    print("Reading conversations.json...")
    for conv in iter_json_array(conv_path):
        conv_id = conv.get("id") or conv.get("conversation_id")
        if not conv_id:
            continue

        mapping = conv.get("mapping") or {}
        node_count = len(mapping)
        message_count = sum(1 for node in mapping.values() if node.get("message"))

        index.append(
            {
                "id": conv_id,
                "title": conv.get("title") or "(untitled)",
                "create_time": conv.get("create_time"),
                "update_time": conv.get("update_time"),
                "current_node": conv.get("current_node"),
                "node_count": node_count,
                "message_count": message_count,
            }
        )

        out_obj = {
            "id": conv_id,
            "title": conv.get("title") or "(untitled)",
            "create_time": conv.get("create_time"),
            "update_time": conv.get("update_time"),
            "current_node": conv.get("current_node"),
            "mapping": mapping,
        }

        out_path = conv_out_dir / f"{conv_id}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(out_obj, f, ensure_ascii=True, separators=(",", ":"))

        total += 1
        if total % 100 == 0:
            print(f"  processed {total} conversations...")

    with (out_dir / "index.json").open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=True, separators=(",", ":"))

    assets = {}
    if chat_path.exists():
        print("Extracting assets from chat.html...")
        assets = extract_assets_json(chat_path)

    with (out_dir / "assets.json").open("w", encoding="utf-8") as f:
        json.dump(assets, f, ensure_ascii=True, separators=(",", ":"))

    template_path = Path(__file__).with_name("chatgpt_viewer_template.html")
    if not template_path.exists():
        raise FileNotFoundError("Missing viewer template: chatgpt_viewer_template.html")

    viewer_path = export_dir / "viewer.html"
    viewer_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")

    print("Done.")
    print(f"Viewer: {viewer_path}")
    print(f"Data: {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Build a static viewer for ChatGPT export data.")
    parser.add_argument("export_dir", help="Path to the ChatGPT export folder")
    args = parser.parse_args()

    export_dir = Path(args.export_dir).expanduser().resolve()
    if not export_dir.exists():
        print(f"Export folder not found: {export_dir}", file=sys.stderr)
        sys.exit(1)

    build_viewer(export_dir)


if __name__ == "__main__":
    main()
