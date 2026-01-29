#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from json import JSONDecoder
from pathlib import Path, PurePosixPath

ASSET_URLS = {
    "marked.min.js": "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
    "purify.min.js": "https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js",
    "katex.min.js": "https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js",
    "auto-render.min.js": "https://cdn.jsdelivr.net/npm/katex/dist/contrib/auto-render.min.js",
    "katex.min.css": "https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css",
}
KATEX_CSS_NAME = "katex.min.css"


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

    ensure_viewer_assets(export_dir)

    template_path = Path(__file__).with_name("chatgpt_viewer_template.html")
    if not template_path.exists():
        raise FileNotFoundError("Missing viewer template: chatgpt_viewer_template.html")

    viewer_path = export_dir / "viewer.html"
    viewer_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")

    print("Done.")
    print(f"Viewer: {viewer_path}")
    print(f"Data: {out_dir}")


def ensure_viewer_assets(export_dir):
    asset_dir = export_dir / "viewer_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)

    print("Checking viewer assets...")
    for name, url in ASSET_URLS.items():
        path = asset_dir / name
        if path.exists() and path.stat().st_size > 0:
            continue
        try:
            download_asset(url, path)
        except Exception as err:
            print(f"  warning: failed to download {url}: {err}")

    css_path = asset_dir / KATEX_CSS_NAME
    if css_path.exists() and css_path.stat().st_size > 0:
        try:
            css_text = css_path.read_text(encoding="utf-8")
            font_paths = extract_css_urls(css_text)
            base_url = ASSET_URLS[KATEX_CSS_NAME].rsplit("/", 1)[0] + "/"
            for font_path in font_paths:
                rel_path = safe_rel_path(font_path)
                if rel_path is None:
                    continue
                dest = asset_dir / rel_path
                if dest.exists() and dest.stat().st_size > 0:
                    continue
                font_url = urllib.parse.urljoin(base_url, font_path)
                try:
                    download_asset(font_url, dest)
                except Exception as err:
                    print(f"  warning: failed to download {font_url}: {err}")
        except Exception as err:
            print(f"  warning: failed to parse KaTeX fonts: {err}")


def download_asset(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {url}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = resp.read()
    if not data:
        raise RuntimeError("empty response")
    dest.write_bytes(data)


def extract_css_urls(css_text):
    matches = re.findall(r"url\\(([^)]+)\\)", css_text)
    urls = []
    for raw in matches:
        cleaned = raw.strip().strip('"').strip("'")
        if not cleaned or cleaned.startswith("data:"):
            continue
        urls.append(cleaned)
    return urls


def safe_rel_path(url_path):
    path = PurePosixPath(url_path)
    if ".." in path.parts:
        return None
    return Path(*path.parts)


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
