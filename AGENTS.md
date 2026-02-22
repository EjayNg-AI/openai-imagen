# IMPORTANT FILES

- scratchpad/other_files/codeblocks_for_normal_api_requests.md
  Instructions on how to call the OpenAI API in Python.

- scratchpad/other_files/codeblocks_for_background_tasks-v2.md
  Instructions on how to call the OpenAI API using background mode.

- scratchpad/other_files/codeblocks_for_json_output.md
  Instructions on JSON schema input/output with the OpenAI API.

- docs/codex_outbound_network_access.md
  Notes on outbound-network precautions and minimum allowlist for local API scripts.

- agent_skills/
  Documentation on setting up agent skills in line with OpenAI's prescriptions.

- .agents/skills/
  Repository-local skill implementations and helper scripts used by Codex.

- .agents/skills/chatgpt-archive-topic-background-report/scripts/run_topic_report.py
  End-to-end topic workflow: archive thread search, research-collection JSON assembly, background API run, and saved report artifacts.

- scratchpad/experiment.py and scratchpad/experiment.html
  General playground for experimenting before touching production code.

- scratchpad/json_output_playground.py and scratchpad/json_output_playground.html
  Playground specifically for JSON input/output behavior.

- scratchpad/prompt.py and scratchpad/prompt_runner.html and scratchpad/system_messages_consolidated.md
  Playground for multi-turn OpenAI API conversations in text format.

- scratchpad/prompt_agent.py and scratchpad/prompt_agent.html and scratchpad/system_messages_consolidated.md and scratchpad/agentic_problem_solver.md
  Playground for multi-turn OpenAI API conversations in agent mode.

---

# Repository Behavior Guidelines

- Prefer Responses API patterns from the codeblock docs for new API work.
- Use `scratchpad/` playground files for experimentation before official implementation files.
- For background jobs, keep monitoring output low-noise by default; only enable verbose polling when explicitly needed.
- Save generated run artifacts under `scratchpad/` unless the task specifies a different output location.
- Keep this file focused on references and behavior guidelines; do not maintain session-by-session change logs here.

---

# When the coding agent is initiated

- Remind the user **only once during each session, after a task has been successfully completed** to execute:
  `python -m pip install -r requirements.txt --upgrade`
- If the coding agent can perform this command on behalf of the user, offer to do so.
