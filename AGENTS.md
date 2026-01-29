# IMPORTANT FILES

- scratchpad/other_files/codeblocks_for_normal_api_requests.md
  Instructions on how to call the OpenAI API in Python

- scratchpad/other_files/codeblocks_for_background_tasks_v2.md
  Instructions on how to call the OpenAI API using background mode

- scratchpad/other_files/codeblocks_for_json_output.md
  Instructions on how to use JSON schema input and elicit JSON output with the OpenAI API

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


---

# Change log for agent-driven edits

** Coding Agent to add in a description of the tasks completed **

NOTE: This is for my reference after each coding session. The descriptions entered here in this section may not be retained to the next coding session. Do **not** use this section to store persistent information for your own reference. You will need to create a new section in this markdown file if you wish to do so (and use a flag to indicate that I should not delete/alter that section).

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
