# ChatGPT Viewer CLI Cheat Sheet

Single-page command matrix for ChatGPT archive viewer tooling.

## Prerequisites

- From repo root: `cd /home/ngejay3046/openai-imagen`
- Python deps installed: `python -m pip install -r requirements.txt --upgrade`
- For live chat calls: `OPENAI_API_KEY` set in environment (for server authoring APIs)

## Command Matrix

| Task | Command | Required args | Common optional args | Notes |
| --- | --- | --- | --- | --- |
| Build viewer from export | `python3 scripts/build_chatgpt_viewer.py export_dir` | `export_dir` | `--output-dir`, `--no-preserve-viewer-data`, `--asset-archive-dir` | Copies offline renderer assets from local canonical archive; no CDN required. |
| Build viewer (force full `viewer_data` regen) | `python3 scripts/build_chatgpt_viewer.py export_dir --no-preserve-viewer-data` | `export_dir` | `--output-dir`, `--asset-archive-dir` | Discards existing live-authored `viewer_data` and regenerates from export. |
| Serve one archive (live API + static) | `python3 scripts/chatgpt_viewer_server.py --viewer-dir site_dir` | `--viewer-dir` | `--host`, `--port`, `--asset-archive-dir` | API prefix: `/api/archive/...` |
| Serve hub for many archives | `python3 scripts/chatgpt_viewer_server.py --sites-root chatgpt_viewer_sites` | `--sites-root` | `--host`, `--port`, `--asset-archive-dir` | Hub at `/`, archive pages at `/archives/<slug>/viewer.html`, API prefix: `/api/archives/<slug>/...` |
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
