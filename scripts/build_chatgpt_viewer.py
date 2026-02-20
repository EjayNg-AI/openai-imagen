#!/usr/bin/env python3
import argparse
import json
import re
import shutil
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
MATHJAX_URL = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
MATHJAX_LOCAL = Path("mathjax") / "tex-svg.js"
DEFAULT_OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "chatgpt_viewer_sites"


def default_output_dir_for_export(export_dir):
    # Keep builds for different raw export folders isolated by default.
    return DEFAULT_OUTPUT_ROOT / export_dir.name


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


def has_existing_viewer_data(out_dir, conv_out_dir):
    if not (out_dir / "index.json").exists():
        return False
    if not conv_out_dir.exists():
        return False
    if any(conv_out_dir.glob("*.json")):
        return True
    return (out_dir / "assets.json").exists()


def build_viewer_data(export_dir, out_dir, conv_out_dir):
    conv_path = export_dir / "conversations.json"
    chat_path = export_dir / "chat.html"
    if not conv_path.exists():
        raise FileNotFoundError(f"Missing conversations.json in {export_dir}")

    conv_out_dir.mkdir(parents=True, exist_ok=True)
    for stale_file in conv_out_dir.glob("*.json"):
        stale_file.unlink()

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

    return assets


def build_viewer(export_dir, output_dir, preserve_viewer_data=True):
    output_dir.mkdir(parents=True, exist_ok=True)

    out_dir = output_dir / "viewer_data"
    conv_out_dir = out_dir / "conversations"

    if preserve_viewer_data and has_existing_viewer_data(out_dir, conv_out_dir):
        print("Preserving existing viewer_data (index.json, conversations/, assets.json).")
        assets_path = out_dir / "assets.json"
        if assets_path.exists():
            try:
                assets = json.loads(assets_path.read_text(encoding="utf-8"))
                if not isinstance(assets, dict):
                    assets = {}
            except Exception:
                assets = {}
        else:
            assets = {}
    else:
        assets = build_viewer_data(export_dir, out_dir, conv_out_dir)

    copy_export_assets(export_dir, output_dir, assets)
    ensure_viewer_assets(output_dir)

    template_path = Path(__file__).with_name("chatgpt_viewer_template.html")
    if not template_path.exists():
        raise FileNotFoundError("Missing viewer template: chatgpt_viewer_template.html")

    viewer_path = output_dir / "viewer.html"
    viewer_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")

    test_template_path = Path(__file__).with_name("chatgpt_render_test_template.html")
    if test_template_path.exists():
        test_path = output_dir / "render_test.html"
        test_path.write_text(test_template_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Render test: {test_path}")
    else:
        print("Render test template missing: chatgpt_render_test_template.html")

    print("Done.")
    print(f"Source export: {export_dir}")
    print(f"Output dir: {output_dir}")
    print(f"Viewer: {viewer_path}")
    print(f"Data: {out_dir}")


def copy_export_assets(export_dir, output_dir, assets):
    if not assets:
        return

    print("Copying referenced export assets...")
    copied = 0
    missing = 0
    skipped = 0
    seen = set()

    for raw_link in assets.values():
        if not isinstance(raw_link, str) or not raw_link:
            continue
        rel_path = safe_rel_path(raw_link)
        if rel_path is None:
            skipped += 1
            continue
        key = rel_path.as_posix()
        if key in seen:
            continue
        seen.add(key)

        src = export_dir / rel_path
        if not src.exists() or not src.is_file():
            missing += 1
            continue
        dest = output_dir / rel_path
        if src.resolve() == dest.resolve():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1

    print(f"  copied {copied} referenced files")
    if missing:
        print(f"  warning: {missing} referenced files were missing in export folder")
    if skipped:
        print(f"  skipped {skipped} non-local asset links")


def ensure_viewer_assets(output_dir):
    asset_dir = output_dir / "viewer_assets"
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
            normalized = css_text.replace("../fonts/", "fonts/")
            if normalized != css_text:
                css_path.write_text(normalized, encoding="utf-8")
                css_text = normalized
            font_paths = extract_css_urls(css_text)
            base_url = ASSET_URLS[KATEX_CSS_NAME].rsplit("/", 1)[0] + "/"
            alt_bases = [
                "https://unpkg.com/katex/dist/",
            ]
            version = extract_katex_version(asset_dir / "katex.min.js")
            if version:
                alt_bases.append(f"https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{version}/")
            for font_path in font_paths:
                rel_path = safe_rel_path(font_path)
                if rel_path is None:
                    continue
                dest = asset_dir / rel_path
                if dest.exists() and dest.stat().st_size > 0:
                    continue
                success = False
                last_err = None
                for base in [base_url] + alt_bases:
                    font_url = urllib.parse.urljoin(base, font_path)
                    try:
                        download_asset(font_url, dest)
                        success = True
                        break
                    except Exception as err:
                        last_err = err
                if not success:
                    print(f"  warning: failed to download font {font_path}: {last_err}")
        except Exception as err:
            print(f"  warning: failed to parse KaTeX fonts: {err}")
        fonts_dir = asset_dir / "fonts"
        if not fonts_dir.exists() or not any(fonts_dir.iterdir()):
            print("  warning: KaTeX fonts missing; check network access and rebuild.")

    mathjax_path = asset_dir / MATHJAX_LOCAL
    if not mathjax_path.exists() or mathjax_path.stat().st_size == 0:
        try:
            download_asset(MATHJAX_URL, mathjax_path)
        except Exception as err:
            print(f"  warning: failed to download {MATHJAX_URL}: {err}")


def download_asset(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {url}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = resp.read()
    if not data:
        raise RuntimeError("empty response")
    dest.write_bytes(data)


def extract_css_urls(css_text):
    matches = re.findall(r"url\(([^)]+)\)", css_text)
    urls = []
    for raw in matches:
        cleaned = raw.strip().strip('"').strip("'")
        if not cleaned or cleaned.startswith("data:"):
            continue
        urls.append(cleaned)
    return urls


def safe_rel_path(url_path):
    parsed = urllib.parse.urlparse(url_path)
    if parsed.scheme or parsed.netloc:
        return None
    path = PurePosixPath(parsed.path)
    if path.is_absolute():
        return None

    parts = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            return None
        parts.append(part)

    if not parts:
        return None
    return Path(*parts)


def extract_katex_version(js_path):
    if not js_path.exists():
        return None
    try:
        text = js_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    match = re.search(r"KaTeX\\s+v?(\\d+\\.\\d+\\.\\d+)", text)
    if match:
        return match.group(1)
    return None


def main():
    parser = argparse.ArgumentParser(description="Build a static viewer for ChatGPT export data.")
    parser.add_argument("export_dir", help="Path to the ChatGPT export folder")
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help=(
            "Directory for generated viewer artifacts (viewer.html, viewer_data, viewer_assets). "
            "Default: <repo>/chatgpt_viewer_sites/<export-folder-name>"
        ),
    )
    parser.add_argument(
        "--preserve-viewer-data",
        dest="preserve_viewer_data",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Preserve existing viewer_data on rebuild (default: enabled). "
            "Use --no-preserve-viewer-data to fully regenerate viewer_data from conversations.json."
        ),
    )
    args = parser.parse_args()

    export_dir = Path(args.export_dir).expanduser().resolve()
    if not export_dir.exists():
        print(f"Export folder not found: {export_dir}", file=sys.stderr)
        sys.exit(1)

    if args.output_dir:
        output_dir = Path(args.output_dir).expanduser().resolve()
    else:
        output_dir = default_output_dir_for_export(export_dir).resolve()
    build_viewer(export_dir, output_dir, preserve_viewer_data=args.preserve_viewer_data)


if __name__ == "__main__":
    main()
