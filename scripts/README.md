# ChatGPT Archive Viewer Tooling

This directory contains the build/server tooling for ChatGPT conversation archive viewers.

Quick command matrix: `docs/chatgpt_viewer_cli_cheat_sheet.md`

## Components

- `build_chatgpt_viewer.py`
: Builds a static viewer site from one ChatGPT export folder.
- `chatgpt_viewer_server.py`
: Runs live authoring API + static hosting in either single-archive or multi-archive hub mode.
- `viewer_asset_utils.py`
: Verifies and maintains the canonical offline renderer asset archive manifest.
- `chatgpt_viewer_template.html`
: Viewer page template copied into each built archive.
- `chatgpt_archive_hub_template.html`
: Hub page template used by multi-archive mode.
- `viewer_asset_archive/`
: Canonical repository-local renderer assets.

## Renderer Asset Policy

Renderer dependencies are local-only and CDN-independent.

- Build/runtime do not download renderer assets from CDN.
- Each archive site gets a local copy at `viewer_assets/`.
- The canonical source is `scripts/viewer_asset_archive/`.
- Integrity is enforced by `scripts/viewer_asset_archive/manifest.json`.
- If local assets are missing at runtime, rendered mode is disabled and the viewer shows an explicit warning banner.

## Command-Line Reference

### `build_chatgpt_viewer.py`

Usage:

```bash
python3 scripts/build_chatgpt_viewer.py \
  [--output-dir OUTPUT_DIR] \
  [--preserve-viewer-data | --no-preserve-viewer-data] \
  [--asset-archive-dir ASSET_ARCHIVE_DIR] \
  export_dir
```

Arguments:

- `export_dir` (required positional)
: Path to ChatGPT export folder (must contain `conversations.json`; optionally `chat.html`).
- `--output-dir`, `-o`
: Output site directory.
  Default: `<repo>/chatgpt_viewer_sites/<export-folder-name>`.
- `--preserve-viewer-data` / `--no-preserve-viewer-data`
: Preserve existing `viewer_data/` on rebuild (default: preserve).
- `--asset-archive-dir`
: Canonical local renderer asset archive to copy from.
  Default: `scripts/viewer_asset_archive`.

Examples:

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27 --output-dir chatgpt_viewer_sites/custom-name
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27 --no-preserve-viewer-data
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27 --asset-archive-dir scripts/viewer_asset_archive
```

### `chatgpt_viewer_server.py`

Usage:

```bash
python3 scripts/chatgpt_viewer_server.py \
  (--viewer-dir VIEWER_DIR | --sites-root SITES_ROOT) \
  [--asset-archive-dir ASSET_ARCHIVE_DIR] \
  [--host HOST] \
  [--port PORT]
```

Arguments:

- `--viewer-dir`, `-d`
: Single-archive mode. Serve one built viewer site folder.
- `--sites-root`
: Multi-archive hub mode. Serve archive hub + archive-scoped routes for all site folders under root.
- `--asset-archive-dir`
: Canonical renderer archive used when creating blank archives in hub mode.
  Default: `scripts/viewer_asset_archive`.
- `--host`
: Bind host. Default: `127.0.0.1`.
- `--port`
: Bind port. Default: `8000`.

Examples:

```bash
# Single archive mode
python3 scripts/chatgpt_viewer_server.py --viewer-dir chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27 --host 127.0.0.1 --port 8000

# Multi-archive hub mode
python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites --host 127.0.0.1 --port 8000

# Multi-archive with explicit asset archive path
python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites --asset-archive-dir scripts/viewer_asset_archive --port 8000
```

### `viewer_asset_utils.py`

Usage:

```bash
python3 scripts/viewer_asset_utils.py \
  [--archive-dir ARCHIVE_DIR] \
  [--write-manifest] \
  [--verify]
```

Arguments:

- `--archive-dir`
: Asset archive directory to operate on.
  Default: `scripts/viewer_asset_archive`.
- `--write-manifest`
: Recompute and write `manifest.json` checksums.
- `--verify`
: Verify archive files against `manifest.json`.

Examples:

```bash
python3 scripts/viewer_asset_utils.py --verify
python3 scripts/viewer_asset_utils.py --write-manifest --verify
```

## Build Output Layout

Each built site directory contains:

- `viewer.html`
- `render_test.html`
- `viewer_data/index.json`
- `viewer_data/assets.json`
- `viewer_data/conversations/*.json`
- `viewer_assets/*` (copied from canonical local archive)

## Server Modes and Routes

### Single-Archive Mode (`--viewer-dir`)

Open:

```text
http://localhost:8000/viewer.html
```

Core routes:

- `GET /api/archive/health`
- `POST /api/archive/chat/new`
- `POST /api/archive/chat/continue`
- `GET /api/archive/chat/background/<response_id>`
- `POST /api/archive/chat/background/<response_id>/cancel`

### Multi-Archive Hub Mode (`--sites-root`)

Open hub:

```text
http://localhost:8000/
```

Hub routes:

- `GET /api/archives`
: List archive sites discovered in `--sites-root`.
- `POST /api/archives`
: Create blank archive site and return open URL.

Archive pages:

- `GET /archives/<slug>/viewer.html`
- `GET /archives/<slug>/<asset_path>`

Archive-scoped live API routes:

- `GET /api/archives/<slug>/health`
- `POST /api/archives/<slug>/chat/new`
- `POST /api/archives/<slug>/chat/continue`
- `GET /api/archives/<slug>/chat/background/<response_id>`
- `POST /api/archives/<slug>/chat/background/<response_id>/cancel`

## Live Chat API Payloads

Chat endpoints accept either:

- `application/json` body (no file attachments), or
- `multipart/form-data` body with `payload_json` (required stringified JSON object) and `attachments` (optional repeated file part; one part per file).

### `chat/new`

Required `payload_json` fields:

- `prompt` (string)

Optional `payload_json` fields:

- `title` (string, max 80 chars)
- `model` (string)
- `reasoning_effort` (`none|low|medium|high|xhigh`)
- `text_verbosity` (`low|medium|high`)
- `background` (boolean)

### `chat/continue`

Required `payload_json` fields:

- `conversation_id` (string)
- `anchor_node_id` (string)
- `prompt` (string)

Optional `payload_json` fields:

- `model` (string)
- `reasoning_effort` (`none|low|medium|high|xhigh`)
- `text_verbosity` (`low|medium|high`)
- `background` (boolean)

### Attachment multipart example

Single-archive route:

```bash
curl -sS -X POST http://127.0.0.1:8000/api/archive/chat/new \
  -F 'payload_json={"prompt":"Summarize these files.","model":"gpt-5.1"}' \
  -F 'attachments=@/path/to/notes.pdf' \
  -F 'attachments=@/path/to/diagram.png'
```

Archive-scoped route:

```bash
curl -sS -X POST http://127.0.0.1:8000/api/archives/<slug>/chat/continue \
  -F 'payload_json={"conversation_id":"<id>","anchor_node_id":"<node>","prompt":"Continue with the attached files."}' \
  -F 'attachments=@/path/to/file1.txt' \
  -F 'attachments=@/path/to/file2.jpg'
```

### Attachment behavior

- Viewer UI keeps a current attachment list per page session.
- Users can add/remove files between turns, and each turn sends the current list.
- Images are uploaded with `purpose="vision"` and attached as `input_image`.
- Non-image files are uploaded with `purpose="user_data"` and attached as `input_file`.
- Uploaded files are cleaned up after foreground requests and after background requests reach a terminal status.

### Background flow

- Submit `chat/new` or `chat/continue` with `background: true`.
- Poll `.../chat/background/<response_id>` until `done=true`.
- Optional cancel via `.../chat/background/<response_id>/cancel`.
- Viewer UI polling interval: 10 seconds.

## End-to-End Workflows

### Build and serve static viewer

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
cd chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27
python3 -m http.server 8000
# open http://localhost:8000/viewer.html
```

### Build and serve live single archive

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
python3 scripts/chatgpt_viewer_server.py --viewer-dir chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27 --port 8000
# open http://localhost:8000/viewer.html
```

### Run multi-archive hub and create blank archives

```bash
python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites --port 8000
# open http://localhost:8000/
```

Optional API create example:

```bash
curl -sS -X POST http://127.0.0.1:8000/api/archives \
  -H 'Content-Type: application/json' \
  -d '{"name":"my new archive"}'
```

## Requirements

- `OPENAI_API_KEY` set in environment for live chat calls.
- Python dependencies installed from `requirements.txt`.

## Persistence and Rebuild Semantics

- Live authoring updates:
  - `viewer_data/index.json`
  - `viewer_data/conversations/<id>.json`
- Default rebuild preserves existing `viewer_data/`.
- Use `--no-preserve-viewer-data` to fully regenerate `viewer_data/` from export.

## Git Notes

- Raw exports (`chatgpt_conversation_history_YYYY-MM-DD/`) are gitignored.
- Build output in `chatgpt_viewer_sites/` is committable.
- Live-authored `viewer_data/*.json` can be committed for cross-device continuity.
- Temporary files are ignored:
  - `viewer_data/*.tmp`
  - `viewer_data/conversations/*.tmp`

## Troubleshooting

- If rendered mode is unavailable, run:

```bash
python3 scripts/viewer_asset_utils.py --verify
```

- If the canonical archive was intentionally changed, run:

```bash
python3 scripts/viewer_asset_utils.py --write-manifest --verify
```

- If browser shows stale viewer content, cache-bust:

```text
http://localhost:8000/viewer.html?ts=1
```
