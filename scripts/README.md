# ChatGPT Export Viewer Builder

This folder contains a small builder script that turns a ChatGPT export
(`conversations.json` + `chat.html`) into a static, searchable viewer.
It generates a lightweight `viewer.html` and a `viewer_data/` directory
that can be served over a local static web server.

## What it does

- Reads `conversations.json` as a stream (safe for large files).
- Extracts asset links from `chat.html`.
- Downloads the offline rendering assets (Markdown + KaTeX) into `viewer_assets/` if missing. The viewer falls back to CDN assets if `viewer_assets/` is not present.
- Writes:
  - `viewer.html` (the UI)
  - `viewer_data/index.json` (conversation metadata)
  - `viewer_data/conversations/<id>.json` (one file per conversation)
  - `viewer_data/assets.json` (asset pointer → local file mapping)
  - `viewer_assets/` (offline Markdown/KaTeX renderer assets)

## Build (from repo root)

```
python scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
```

This writes the viewer output into the export folder.

## Run (from the export folder)

```
cd chatgpt_conversation_history_2026-01-27
python -m http.server 8000
```

Then open:

```
http://localhost:8000/viewer.html
```

If you don’t see changes after rebuilding, cache‑bust:

```
http://localhost:8000/viewer.html?ts=1
```

## UI notes

- Tree nodes are left‑aligned (no hierarchy indentation).
- System/tool content is hidden by default; toggle it on as needed.
- Dark mode is available and persists in local storage.
- The transcript auto‑scrolls to the selected node.
- Enable "Rendered view" for Markdown + LaTeX rendering (works offline after assets download).
