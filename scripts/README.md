# ChatGPT Export Viewer Builder

This folder contains a builder script that turns a ChatGPT export
(`conversations.json` + `chat.html`) into a static, searchable viewer.

It keeps raw export folders ignored while writing commit-friendly viewer
bundles outside those folders by default.

## What it does

- Reads `conversations.json` as a stream (safe for large files).
- Extracts asset links from `chat.html`.
- Copies referenced export assets into the output bundle so attachment links resolve.
- Downloads offline rendering assets (Markdown + KaTeX + MathJax) into
  `viewer_assets/` if missing. The viewer falls back to CDN assets if these
  files are not present.
- Writes:
  - `viewer.html` (the UI)
  - `viewer_data/index.json` (conversation metadata)
  - `viewer_data/conversations/<id>.json` (one file per conversation)
  - `viewer_data/assets.json` (asset pointer -> local file mapping)
  - `viewer_assets/` (offline renderer assets)
- Supports live authoring via `scripts/chatgpt_viewer_server.py`, including:
  - creating a new conversation directly in the built archive
  - creating new turns in existing conversations by branching from the selected node
  - persisting those additions back into `viewer_data/`

## Build (from repo root)

Default output directory is per-export:
`chatgpt_viewer_sites/<export-folder-name>/`.

Example:

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
```

Optional explicit output directory:

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27 --output-dir chatgpt_viewer_sites/custom-name
```

Rebuild safety default:
- Existing `viewer_data/` is preserved by default, so live-added conversations/turns are not overwritten on rebuild.
- To fully regenerate `viewer_data/` from the raw export, pass:

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27 --no-preserve-viewer-data
```

## Run (from the viewer output folder)

```bash
cd chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/viewer.html
```

## Live chat authoring (new + continue turns)

Use the dedicated viewer server (not `python -m http.server`) when you want to:
- create a new conversation inside the built archive
- create new turns in an existing archive conversation from the selected tree node

The server writes updates to `viewer_data/` in the selected viewer site folder.
Those updates persist across browser reloads and server restarts because they are written to disk.

Example:

```bash
python3 scripts/chatgpt_viewer_server.py --viewer-dir chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27 --port 8000
```

Then open:

```text
http://localhost:8000/viewer.html
```

Requirements:
- `OPENAI_API_KEY` must be set
- install dependencies from `requirements.txt`

## Persistence + rebuild behavior

- Live authoring writes to:
  - `viewer_data/index.json`
  - `viewer_data/conversations/<id>.json`
- Default rebuild behavior is safe for live additions:
  - `python3 scripts/build_chatgpt_viewer.py <export_dir>` preserves existing `viewer_data/` if present.
- To intentionally discard live additions and regenerate `viewer_data/` from raw export:
  - `python3 scripts/build_chatgpt_viewer.py <export_dir> --no-preserve-viewer-data`

If you do not see changes after rebuilding, cache-bust:

```text
http://localhost:8000/viewer.html?ts=1
```

The rendering test page is also generated:

```text
http://localhost:8000/render_test.html?ts=1
```

## Rebuild + reload sequence

```bash
python3 scripts/build_chatgpt_viewer.py chatgpt_conversation_history_2026-01-27
cd chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27
python3 -m http.server 8000
```

Then reload with:

```text
http://localhost:8000/viewer.html?ts=1
```

## Git note

- Raw exports like `chatgpt_conversation_history_YYYY-MM-DD/` are gitignored.
- Build output in `chatgpt_viewer_sites/` can be committed.
- Live-authored conversation updates in `viewer_data/` are committable, so you can push
  new conversations/turns and continue from another machine.
- Temporary files are gitignored:
  - `viewer_data/*.tmp`
  - `viewer_data/conversations/*.tmp`
- Different raw export folders build to different default output folders, so
  builds can coexist without overwriting each other.
- Legacy `chatgpt_viewer_site/` is deprecated and gitignored.

## UI notes

- Tree nodes are left-aligned (no hierarchy indentation).
- System/tool content is hidden by default; toggle it on as needed.
- Dark mode is available and persists in local storage.
- The transcript auto-scrolls to the selected node.
- Enable "Rendered view" for Markdown + LaTeX rendering (works offline once
  `viewer_assets/` is present).
- Use the math renderer dropdown to switch between KaTeX (HTML) and MathJax (SVG).
