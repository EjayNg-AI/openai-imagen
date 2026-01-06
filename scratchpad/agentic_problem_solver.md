# Agentic Problem Solver Workflow

This document describes the agentic math problem-solving workflow implemented in the prompt runner UI and backend. It covers UI flow, agent sequencing, structured-output orchestration, persistence, and error/resume behavior.

## Overview

The workflow is an agent-driven multi-stage pipeline for mathematical problems. It uses a single developer message box plus a user problem statement, then drives agent stages via the Responses API using the model/settings selected in the UI.

Two workflows are supported:

- With approaches: Approach Proposer -> Approach Evaluator -> Problem Solver -> Expert Solution Evaluator -> Orchestrator.
- Without approaches: Problem Solver -> Expert Solution Evaluator -> Orchestrator.

After each Solver/Evaluator loop, the Orchestrator runs with JSON schema structured output to decide whether to dispatch another loop, finalize, or ask the user.

## Files and Routes

- UI: `scratchpad/prompt_agent.html`
- Backend: `scratchpad/prompt_agent.py`
- Orchestrator schema and system messages: `scratchpad/system_messages_consolidated.md`
- Saved state: `scratchpad/saved_snapshots/agentic_workflow_state.json` (default; filename configurable in UI)
- Snapshot store: `scratchpad/saved_snapshots/` (versioned snapshot files)

Routes added/used:

- UI served from `/` and `/prompt-runner` (both serve `scratchpad/prompt_agent.html`).
- System messages: `/api/system-message/<key>`
- Standard prompt run: `/api/prompt-run` and `/api/prompt-run-background`
- Orchestrator run (structured output): `/api/orchestrator-run` and `/api/orchestrator-run-background`
- Orchestrator polling/cancel: `/api/orchestrator-run-background/<response_id>` and `/api/orchestrator-run-background/<response_id>/cancel`
- State persistence: `/api/agentic-state` (GET/POST, optional `filename` query param)
- Snapshot listing: `/api/agentic-snapshots` (GET, requires `filename` query param)
- Snapshot load/save: `/api/agentic-snapshot` (GET/POST)

## UI Controls and Panels

New UI controls in `scratchpad/prompt_agent.html`:

- Initiate agentic workflow with approaches
- Initiate agentic workflow without approaches
- Resume agentic workflow
- Save current state
- Stop workflow (cancels the in-flight request and pauses the workflow)
- Auto-advance workflow (auto-accepts Yes prompts)
- Max solver/evaluator loops (auto) limit for autonomous runs
- Saved snapshots selector
- Refresh snapshots
- Rollback to snapshot
- Resume from snapshot

Workflow prompt panel:

- After each agent stage, the UI asks whether to proceed (Yes/No).
- "No" pauses the workflow and saves state.
- When auto-advance is enabled, prompts are auto-accepted until the loop limit is reached.
- Resume actions always prompt for confirmation and specify the next agent before continuing.

Orchestrator output panel:

- Displays parsed JSON in a textarea and a rendered HTML view.
- Copy button copies the JSON text.

## Input Validation and Auto-Correction

When starting a workflow:

- The first message row is forced to role Developer and the second to role User.
- If the second message is empty, the workflow fails with an error.
- The user problem statement must include one of: "problem", "question", or "research" (case-insensitive).
- All additional message rows are removed before the workflow begins (clears the deck).

If validation fails, the workflow does not start and an error is shown.

## Agent Stage Execution

For each stage:

- The developer message box is overwritten with the appropriate system message fetched via `/api/system-message/<key>`.
- The call uses the current UI settings: model, reasoning effort, verbosity, and background mode.
- The assistant output is copied into a new input box as a User message (not Assistant).
- After each stage, the UI prompts the user to proceed.

System message keys used:

- `approach-proposer`
- `approach-evaluator`
- `problem-solver`
- `expert-evaluator`
- `orchestrator`

## Orchestrator Structured Output

After each Solver/Evaluator loop, the Orchestrator runs with JSON schema output:

- The backend loads the schema under `# SCHEMA FOR ORCHESTRA API CALL` from `scratchpad/system_messages_consolidated.md`.
- The API request uses `text.format.type = "json_schema"`, `strict = true`, and the schema payload.
- The orchestrator response is parsed as JSON; parse errors halt the workflow.
- The parsed JSON is rendered in the UI and saved in workflow state.

If the orchestrator action is `FINAL` or `ASK_USER`, the workflow auto-ends, saves state, and displays the JSON decision. Otherwise, the UI asks whether to run another Solver/Evaluator loop.

## Error Handling

At any stage:

- Errors are displayed in the status area.
- The workflow state is saved automatically with the error metadata.
- In autonomous mode, the system retries once for any error except orchestrator JSON parse errors.
- On a second error in the same stage, autonomous mode stops the workflow and reports the failure.
- Orchestrator JSON parse errors do not retry.
- Resume re-runs the failed stage using the same developer and user inputs.

Background mode errors and cancellations are also surfaced, and the workflow state is preserved for resumption.

## Persistence and Resume Behavior

State is saved to a JSON file in `scratchpad/saved_snapshots/`. The filename is taken from the Workflow filename field and defaults to `agentic_workflow_state.json` (single file per name, overwritten on each save). Legacy state files in `scratchpad/` are still readable, but new saves write to `scratchpad/saved_snapshots/`.

The saved state includes:

- All message rows and roles
- Current model/verbosity/reasoning/background settings
- Workflow queue, last stage, loop count, and error info
- Latest parsed orchestrator JSON output
- Selected workflow filename (for future saves)

Snapshot behavior:

- Snapshots are stored as versioned JSON files in `scratchpad/saved_snapshots/`.
- Snapshot filenames are `[workflow_filename_stem]_[label].json`, where label includes timestamp plus note/loop/stage hints.
- Filename examples:
  - `agentic_workflow_state_2025-01-17T18-42-05-123Z_manual_loop-0_stage-orchestrator.json`
  - `my_workflow_2025-01-17T18-42-05Z_rollback_loop-2_stage-expert-evaluator.json`
- Snapshots are created only on manual save and rollback actions (auto-saves do not create snapshots).
- The snapshot list is filtered by the current Workflow filename.
- The state file in `scratchpad/saved_snapshots/` is the mutable “current working copy” overwritten on each save/auto-save.
- Snapshots are immutable history entries; they are never overwritten and are only created manually or via rollback.

Resume behavior:

- "Resume agentic workflow" loads the saved state from the server file named in the Workflow filename field.
- Resume prompts for confirmation and explicitly names the next agent before continuing.
- If the saved queue is empty, Resume seeds a default Problem Solver -> Expert Evaluator -> Orchestrator loop before prompting.
- If a stage was pending or failed, it continues or re-runs that stage after confirmation.
- If the workflow is marked complete and still has a queue, Resume reports completion and does not continue.

Manual saves:

- The Save button is always enabled and writes the current state.
- Manual saves also create a snapshot version.
- Automatic saves occur on errors, when pausing, and after orchestrator completion (no snapshot version).

## Resume vs Rollback (Detailed)

Use these controls when multiple checkpoints exist:

- Resume agentic workflow
  - Loads the latest state file for the current Workflow filename.
  - If the queue is empty, seeds a Problem Solver -> Expert Evaluator -> Orchestrator loop before prompting.
  - Shows a confirmation prompt that names the next agent.
  - On confirmation, runs the next stage.
- Rollback to snapshot
  - Loads the selected snapshot into the UI and overwrites the main state file.
  - Creates a new snapshot version labeled as a rollback.
  - Does not run any stage automatically.
- Resume from snapshot
  - Loads the selected snapshot into the UI without creating a new snapshot version.
  - If the queue is empty, seeds a Problem Solver -> Expert Evaluator -> Orchestrator loop before prompting.
  - Shows a confirmation prompt that names the next agent.
  - On confirmation, writes the main state file and runs the next stage.

## Notes and Limitations

- Persistence uses a single server-side file and is not multi-user safe.
- Background mode polling interval is 60 seconds.
- The normal "Send to OpenAI" button remains available for non-agentic runs.
