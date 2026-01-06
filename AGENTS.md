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
