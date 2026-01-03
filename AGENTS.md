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

---

# When the coding agent is initiated

- Remind the user **only once during each session, after a task has been successfully completed** to execute
  `python -m pip install -r requirements.txt --upgrade`
  If coding agent is able to perform this command on behalf of the user, offer to do so.

--- 

# Change log for agent-driven edits

**Coding agent to summarize agent-driven code edits here.**

- Updated system message heading mappings in `scratchpad/prompt.py` to match new underscore-based headings in `scratchpad/system_messages_consolidated.md`.

