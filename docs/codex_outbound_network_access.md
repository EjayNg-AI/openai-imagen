# Codex Outbound Network Access Notes

This note captures the practical findings for running API-calling scripts from the Codex harness (local sandboxed process), with special focus on OpenAI Responses API usage.

## Why this matters

There are two distinct network paths:

- Built-in chat browsing tools (`web.search`, `web.open`) run in the harness tool environment.
- Local commands (for example `python -u scratchpad/background_mode_gpt52_test.py`) run in the workspace process sandbox and require outbound access from that runtime.

A web search can succeed while a local Python API call still fails if outbound access is blocked for local command execution.

## OpenAI guidance summary (Codex docs)

From OpenAI Codex security/internet-access docs:

- Network access is restricted by default and should be enabled with least privilege.
- Treat internet content as untrusted input (prompt-injection and data exfiltration risk).
- Prefer scoped outbound policy (domain allowlist, restricted methods where possible).
- Review logs and generated changes before trusting outputs.
- Broad unsafe execution modes should be used cautiously.

## Minimal allowlist for this repository's OpenAI API calls

For `scratchpad/background_mode_gpt52_test.py` and similar Responses API scripts:

- Domain allowlist:
  - `api.openai.com`
- Required methods:
  - `POST` for `POST /v1/responses`
  - `GET` for `GET /v1/responses/{response_id}` polling
- Optional method/path:
  - `POST /v1/responses/{response_id}/cancel` if cancellation is needed

If policy allows only `GET/HEAD/OPTIONS`, request creation will fail because `POST` is required.

## Known good command

```bash
python -u scratchpad/background_mode_gpt52_test.py
```

## References

- https://developers.openai.com/codex/cloud/internet-access
- https://developers.openai.com/codex/security
- https://developers.openai.com/codex/changelog
- https://platform.openai.com/docs/api-reference/responses/compact/
