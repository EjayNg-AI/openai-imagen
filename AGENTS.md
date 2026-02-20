# IMPORTANT FILES

- scratchpad/other_files/codeblocks_for_normal_api_requests.md
  Instructions on how to call the OpenAI API in Python

- scratchpad/other_files/codeblocks_for_background_tasks-v2.md
  Instructions on how to call the OpenAI API using background mode

- scratchpad/other_files/codeblocks_for_json_output.md
  Instructions on how to use JSON schema input and elicit JSON output with the OpenAI API

- scratchpad/background_mode_gpt52_test.py
  Background-mode GPT-5.2 test harness that submits a complex prompt with high reasoning effort, polls every 10 seconds, and writes a markdown report to `scratchpad/background_mode_gpt52_test_report.md`. Run it with:
  `python -u scratchpad/background_mode_gpt52_test.py`

- docs/codex_outbound_network_access.md
  Notes on Codex outbound-network precautions and the minimal domain allowlist for OpenAI Responses API calls from local scripts (including required `POST` + `GET` methods for `api.openai.com`).

- scratchpad/experiment.py and scratchpad/experiment.html
  Playground for testing out new features. Safely experiment with code alterations and implementing new features with these playground files first before actual implementation with official code files.

- scratchpad/json_output_playground.py and scratchpad/json_output_playground.html 
  Playground for testing out JSON input and output.

- scratchpad/prompt.py and scratchpad/prompt_runner.html and scratchpad/system_messages_consolidated.md
  Playground for executing multi-turn conversations with the OpenAI API in text format. The system messages that can be loaded into the developer input box is stored in the markdown file.

- scratchpad/prompt_agent.py and scratchpad/prompt_agent.html and scratchpad/system_messages_consolidated.md and scratchpad/agentic_problem_solver.md
  Playground for executing multi-turn conversations with the OpenAI API in agent mode. The system messages that can be loaded into the developer input box is stored in the markdown file scratchpad/system_messages_consolidated.md. The file scratchpad/agentic_problem_solver.md contains an outline of how the agent mode operates.

---

# When the coding agent is initiated

- Remind the user **only once during each session, after a task has been successfully completed** to execute
  `python -m pip install -r requirements.txt --upgrade`
  If coding agent is able to perform this command on behalf of the user, offer to do so.


---

# Persistent Information for Coding Agent

**The coding agent may use this to store persistent information it needs to carry over to the next coding section.** 

I will not delete/alter anything in this section unless I notify you beforehand.

## [DO NOT DELETE/ALTER] Codex Restart Checkpoint - 2026-02-20

### Scope completed in this session

1. ChatGPT archive viewer now supports a **live composer UI** in `scripts/chatgpt_viewer_template.html` for:
   - New conversation creation
   - Continuing selected conversation node (branching from selected node)
   - Model/reasoning/verbosity/background controls (saved in localStorage)
   - Background polling and cancellation UX

2. Added a dedicated backend server `scripts/chatgpt_viewer_server.py` that:
   - Serves viewer static files from a built site folder
   - Calls OpenAI Responses API for new/continue chat
   - Persists generated turns into `viewer_data/` (`index.json` + `conversations/<id>.json`)
   - Exposes endpoints:
     - `POST /api/archive/chat/new`
     - `POST /api/archive/chat/continue`
     - `GET /api/archive/chat/background/<response_id>`
     - `POST /api/archive/chat/background/<response_id>/cancel`
     - `GET /api/archive/health`
   - Enforces context normalization to user/assistant only and strict alternating sequence, with payload beginning and ending with user before API call.

3. Updated docs in `scripts/README.md` with live server usage:
   - `python3 scripts/chatgpt_viewer_server.py --viewer-dir <path> --port 8000`

4. Rebuilt both tracked viewer outputs so template changes are reflected:
   - `chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27/viewer.html`
   - `chatgpt_viewer_sites/chatgpt_conversation_history_2026-02-20/viewer.html`

5. Updated `requirements.txt` to explicitly include Flask core runtime deps plus dotenv:
   - `flask`
   - `blinker`
   - `click`
   - `itsdangerous`
   - `jinja2`
   - `markupsafe`
   - `werkzeug`
   - `python-dotenv`

### Important runtime note

- In this Codex environment, `flask` was not installed, so server runtime endpoints were not end-to-end exercised here.
- `scripts/chatgpt_viewer_server.py` compile check passed (`py_compile`), and it now exits with a clear message if dependencies are missing.

### Working tree state at checkpoint

Modified tracked files:
- `chatgpt_viewer_sites/chatgpt_conversation_history_2026-01-27/viewer.html`
- `chatgpt_viewer_sites/chatgpt_conversation_history_2026-02-20/viewer.html`
- `requirements.txt`
- `scripts/README.md`
- `scripts/chatgpt_viewer_template.html`

Untracked files/folders currently present:
- `scripts/chatgpt_viewer_server.py`
- `cleanup_zone_ids.py`
- `.agents/`

### Resume procedure for next Codex session

1. Install deps:
   - `python -m pip install -r requirements.txt --upgrade`
2. Start live viewer server (example):
   - `python3 scripts/chatgpt_viewer_server.py --viewer-dir chatgpt_viewer_sites/chatgpt_conversation_history_2026-02-20 --port 8000`
3. Open:
   - `http://localhost:8000/viewer.html`
4. Smoke-test:
   - Create new conversation from composer.
   - Continue selected node in existing conversation.
   - Test both foreground and background modes.

### Known follow-up checks (if needed)

- Confirm strict alternation behavior against a few legacy conversations with mixed/system/tool nodes.
- Confirm background job persistence happens exactly once on completion.
- If committing, include both updated tracked `viewer.html` files since this repo tracks built viewer artifacts.


---

# Change log for agent-driven edits

** Coding Agent to add in a description of the tasks completed **

NOTE: This is for my reference after each coding session. The descriptions entered here in this section may not be retained to the next coding session. Do **not** use this section to store persistent information for your own reference. You will need to create a new section in this markdown file if you wish to do so (and use a flag to indicate that I should not delete/alter that section).

- Added `scratchpad/background_mode_gpt52_test.py`, a GPT-5.2 background-mode test script with reasoning effort set to high, 10-second polling, and markdown report logging for status updates plus final output payload. Command: `python -u scratchpad/background_mode_gpt52_test.py`.
- Added `docs/codex_outbound_network_access.md` and README link documenting Codex outbound-network precautions plus the minimal allowlist for successful OpenAI Responses API calls (`api.openai.com` with `POST` and `GET`).
- Added resume-time queue normalization to append the orchestrator after the expert evaluator when missing.
- Added rendered-view toggle with markdown + LaTeX rendering support in the viewer template.
- Added offline renderer asset download in build script and local asset wiring in template/README.
- Added CDN fallback loader when offline renderer assets are missing.
- Added optional LaTeX bracket escape toggle applied only in rendered view outside code blocks.
- Added heuristic math detection for bracket escaping to preserve likely math inside delimiters.
- Expanded math heuristic to treat alphanumeric strings (e.g., 123, 1a2b) as math.
- Expanded math heuristic to treat underscores/carets in standalone tokens as math.
- Moved LaTeX delimiter escaping to pre-Markdown processing and enabled KaTeX \\( \\) / \\[ \\] delimiters.
- Expanded math heuristic to treat numeric forms with decimals/commas as math.
- Added math-block replacement for \\; to \\  (space) in rendered view, including $/$$ segments.
- Normalized newlines inside math blocks before Markdown to prevent KaTeX delimiters from splitting across <br>.
- Added word-wrap rules for transcript/rendered text while preserving code/math formatting.
- Added unsafe code-wrap toggle and safe-mode copy buttons for code blocks.
- Added standalone render test template and build output, plus README rebuild/reload steps.
- Tightened Markdown sanitization configuration and KaTeX safety options.
- Allowed safe SVG tags/attrs in sanitization and expanded render test samples with dangerous-tag code and SVG.
- Escaped the sample </script> string in render test template to avoid breaking the page script.
- Broadened math detection to treat backslash escapes (e.g., \\;) as math.
- Fixed KaTeX font download paths and preserved double backslashes inside math blocks.
- Added MathJax (SVG) toggle, loader, and MathJax asset download support.
- Fixed MathJax loader to avoid skipping script when only config object exists.
- Added KaTeX font download warning when fonts are still missing.
- Fixed MathJax processing class and removed \\; line-break replacement; added KaTeX font download fallbacks.
- Fixed KaTeX font URL extraction and ensured MathJax waits for startup promise.
- Preserved backslash spacing commands inside math and removed MathJax processHtmlClass restriction.
- Built a static ChatGPT export viewer (tree + transcript) with a build script and HTML template.
- Updated the viewer template to add independent scrolling, flat tree alignment, and a dark mode toggle.
- Added auto-scroll to the selected message when a tree node is clicked.
- Added scripts/README.md and ignored export viewer data in .gitignore.
- Added a condensed quadratic assignment with 16 harder questions in latex/c_harder.tex.
- Embedded solutions alongside questions in latex/c_harder.tex, switched to two-column footnotesize layout, and updated the title.
- Added `docs/background_mode_gpt52_codex_harness_summary.md` documenting the prior Codex harness background-mode test workflow, including unbuffered `-u` console behavior, outbound allowlist guidance, and a full verbatim copy of `scratchpad/background_mode_gpt52_test.py`.
- Updated ChatGPT viewer build workflow to keep `chatgpt_conversation_history_YYYY-MM-DD/` exports fully gitignored while writing commit-ready viewer artifacts (later superseded by `chatgpt_viewer_sites/<export-folder-name>/`), including copied referenced assets and offline Markdown/LaTeX renderer assets.
- Updated ChatGPT viewer default output routing to `chatgpt_viewer_sites/<export-folder-name>/` so builds from different raw export directories are isolated and do not overwrite each other.
- Resumed from checkpoint and smoke-tested `scripts/chatgpt_viewer_server.py` locally: verified `/api/archive/health`, static `viewer.html`, and request validation behavior.
- Ran end-to-end live chat authoring checks in a temporary viewer-site copy (to avoid repo mutations): foreground `chat/new`, foreground `chat/continue`, and background create+poll all returned successful persisted results.
- Verified explicit outbound access path to `api.openai.com` with a minimal Responses API background create+retrieve test that completed successfully.
- Added `--preserve-viewer-data` / `--no-preserve-viewer-data` to `scripts/build_chatgpt_viewer.py` with safe default preserve behavior so rebuilds do not overwrite live-added `viewer_data` conversations and turns.
- Updated `scripts/README.md` build docs to document the new preserve-by-default behavior and full-regeneration opt-out flag.
- Expanded `scripts/README.md` documentation to explicitly describe live authoring in existing archives (new conversations + new turns from selected nodes), on-disk persistence, and rebuild safety semantics.
- Updated top-level `README.md` playground section with ChatGPT archive viewer workflow and preserve-by-default rebuild note (`--no-preserve-viewer-data` for full regeneration).
- Updated `.gitignore` to ignore mutable live-authoring viewer data (`chatgpt_viewer_sites/**/viewer_data/index.json`, `conversations/*.json`, and `*.tmp`) so local turn additions are not accidentally staged as new files.
- Updated `scripts/README.md` Git note to document the new `.gitignore` behavior for mutable `viewer_data` files.
- Revised `.gitignore` policy to keep live `viewer_data` conversation/index JSON files committable for cross-device sync, while still ignoring only temporary `*.tmp` runtime files.
