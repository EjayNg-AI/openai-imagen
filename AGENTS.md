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

# Instructions for the coding agent for this session

These instructions apply to the current session only. They will not persist to future sessions.

- The following files have been cloned before the start of this session:
  - scratchpad/prompt.py --> scratchpad/prompt_agent.py
  - scratchpad/prompt_runner.html --> scratchpad/prompt_agent.html
  No modifications have been made to these files yet. These are exact copies of the original files.

- In this session, you are to make modifications to the cloned files only.
  The original files must remain unmodified.

- In this session, you have to refer to the instructions on how to use JSON schema input and elicit JSON output with the OpenAI API. You can also refer to the playground files for testing out JSON input and output for practical implementation of JSON input and output.

- Further instructions will be provided by the user.

---

# Change log for agent-driven edits

**Coding agent to summarize agent-driven code edits here.**

- Updated system message heading mappings in `scratchpad/prompt.py` to match new underscore-based headings in `scratchpad/system_messages_consolidated.md`.

