# IMPORTANT REFERENCE FILES

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

---

# When the coding agent is initiated

- Remind the user to execute
  `python -m pip install -r requirements.txt --upgrade`
  If coding agent is able to perform this command on behalf of the user, offer to do so.

--- 

# Change log for agent-driven edits

**Coding agent to summarize agent-driven code edits here.**
- 2025-12-30: Added outpaint-with-mask mode to `app.py` and `templates/index.html`, including fixed canvas sizes, mask validation, and drag placement UI while keeping standard edit/inpaint flows intact.
- 2025-12-30: Detect edit output image format from bytes to ensure previews and saved files use the correct MIME/extension (fixes inpainting display issues with non-PNG inputs).
- 2025-12-30: Added dedicated error panels in the UI so generate/edit failures and validation issues are displayed clearly in-browser.
- 2025-12-30: Added error.log handling with request-context logging and unhandled exception capture; updated .gitignore for the new log file.
- 2025-12-30: Trim app.log and error.log after each image API call, keeping the most recent 100 lines when logs exceed 200 lines.
- 2026-01-03: Added system-message loader buttons to `scratchpad/prompt_runner_background.html` and documented consolidated system-message keys in `README.md`.
