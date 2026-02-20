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

## Run (from the viewer output folder)

```bash
cd chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/viewer.html
```

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
- Build output in `chatgpt_viewer_sites/` is not gitignored, so it can be committed.
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
