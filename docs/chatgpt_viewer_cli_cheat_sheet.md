# ChatGPT Viewer CLI Cheat Sheet

Single-page command matrix for ChatGPT archive viewer tooling.

## Prerequisites

- From repo root: `cd /home/jenni/openai-imagen`
- Python deps installed: `python -m pip install -r requirements.txt --upgrade`
- For live chat calls: `OPENAI_API_KEY` set in environment (for server authoring APIs)

## Command Matrix

| Task | Command | Required args | Common optional args | Notes |
| --- | --- | --- | --- | --- |
| Build viewer from export | `python3 scripts/build_chatgpt_viewer.py export_dir` | `export_dir` | `--output-dir`, `--no-preserve-viewer-data`, `--asset-archive-dir` | Copies offline renderer assets from local canonical archive; no CDN required. |
| Build viewer (force full `viewer_data` regen) | `python3 scripts/build_chatgpt_viewer.py export_dir --no-preserve-viewer-data` | `export_dir` | `--output-dir`, `--asset-archive-dir` | Discards existing live-authored `viewer_data` and regenerates from export. |
| Serve one archive (live API + static) | `python3 scripts/chatgpt_viewer_server.py --viewer-dir site_dir` | `--viewer-dir` | `--host`, `--port`, `--asset-archive-dir` | API prefix: `/api/archive/...`; chat endpoints accept JSON or multipart (`payload_json` + `attachments`). |
| Serve hub for many archives | `python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites` | `--sites-root` | `--host`, `--port`, `--asset-archive-dir` | Hub at `/`, archive pages at `/archives/<slug>/viewer.html`, API prefix: `/api/archives/<slug>/...`; chat endpoints accept JSON or multipart. |
| Verify canonical renderer assets | `python3 scripts/viewer_asset_utils.py --verify` | none | `--archive-dir` | Validates files against `manifest.json` checksums. |
| Recompute + verify renderer manifest | `python3 scripts/viewer_asset_utils.py --write-manifest --verify` | none | `--archive-dir` | Use only when intentionally changing canonical assets. |

## Argument Reference

### `scripts/build_chatgpt_viewer.py`

```text
python3 scripts/build_chatgpt_viewer.py \
  [--output-dir OUTPUT_DIR] \
  [--preserve-viewer-data | --no-preserve-viewer-data] \
  [--asset-archive-dir ASSET_ARCHIVE_DIR] \
  export_dir
```

- `export_dir`: ChatGPT export folder path.
- `--output-dir`, `-o`: output site folder.
- `--preserve-viewer-data` / `--no-preserve-viewer-data`: preserve (default) or regenerate `viewer_data`.
- `--asset-archive-dir`: source folder for canonical local renderer assets.

### `scripts/chatgpt_viewer_server.py`

```text
python3 scripts/chatgpt_viewer_server.py \
  (--viewer-dir VIEWER_DIR | --sites-root SITES_ROOT) \
  [--asset-archive-dir ASSET_ARCHIVE_DIR] \
  [--host HOST] \
  [--port PORT]
```

- `--viewer-dir`, `-d`: single-archive mode.
- `--sites-root`: multi-archive hub mode.
- `--asset-archive-dir`: canonical renderer archive used for blank archive creation in hub mode.
- `--host`: bind host (default `127.0.0.1`).
- `--port`: bind port (default `8000`).

### `scripts/viewer_asset_utils.py`

```text
python3 scripts/viewer_asset_utils.py \
  [--archive-dir ARCHIVE_DIR] \
  [--write-manifest] \
  [--verify]
```

- `--archive-dir`: archive folder to operate on.
- `--write-manifest`: regenerate `manifest.json`.
- `--verify`: checksum validation.

## Quick URLs

- Single-archive viewer page: `http://127.0.0.1:8000/viewer.html`
- Multi-archive hub page: `http://127.0.0.1:8000/`
- Multi-archive viewer page: `http://127.0.0.1:8000/archives/<slug>/viewer.html`

## Live Chat API Quick Reference

### Endpoints

- Single archive:
  - `POST /api/archive/chat/new`
  - `POST /api/archive/chat/continue`
  - `GET /api/archive/chat/background/<response_id>`
  - `POST /api/archive/chat/background/<response_id>/cancel`
- Archive-scoped (hub mode):
  - `POST /api/archives/<slug>/chat/new`
  - `POST /api/archives/<slug>/chat/continue`
  - `GET /api/archives/<slug>/chat/background/<response_id>`
  - `POST /api/archives/<slug>/chat/background/<response_id>/cancel`

### Request shapes

- JSON (no files): send normal JSON body (`prompt`, `model`, etc.).
- Multipart (with files):
  - `payload_json`: required JSON string with chat fields.
  - `attachments`: optional repeated file part (one part per file).

### Attachment behavior

- The viewer keeps a mutable attachment list in the composer.
- Users can add/remove files between turns; each send uses the current list.
- Image files are uploaded with `purpose="vision"` and sent as `input_image`.
- Non-image files are uploaded with `purpose="user_data"` and sent as `input_file`.
- Uploaded OpenAI file objects are deleted after foreground requests and after background jobs reach terminal status.

### Multipart examples

```bash
curl -sS -X POST http://127.0.0.1:8000/api/archive/chat/new \
  -F 'payload_json={"prompt":"Summarize these files.","model":"gpt-5.1"}' \
  -F 'attachments=@/path/to/notes.pdf' \
  -F 'attachments=@/path/to/diagram.png'
```

```bash
curl -sS -X POST http://127.0.0.1:8000/api/archives/<slug>/chat/continue \
  -F 'payload_json={"conversation_id":"<id>","anchor_node_id":"<node>","prompt":"Continue with the attached files."}' \
  -F 'attachments=@/path/to/file1.txt' \
  -F 'attachments=@/path/to/file2.jpg'
```

## Typical Workflows

### 1) Build + live serve one archive

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
python3 scripts/chatgpt_viewer_server.py --viewer-dir chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27 --port 8000
```

### 2) Start multi-archive hub

```bash
python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites --port 8000
```

### 3) Validate local renderer assets

```bash
python3 scripts/viewer_asset_utils.py --verify
```

## Related Docs

- Detailed viewer tooling reference: `scripts/README.md`
- Repository overview: `README.md`
