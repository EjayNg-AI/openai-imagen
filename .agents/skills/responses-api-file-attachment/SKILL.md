---
name: responses-api-file-attachment
description: Upload and attach local files to OpenAI Responses API requests using Files API with input_file or input_image content items, then manage lifecycle cleanup and optional background polling. Use when users ask how to send PDFs, images, or other local files with Responses API calls, combine file-plus-text prompts, or troubleshoot file_id and image_file_id request shapes.
---

# Responses API File Attachment

Use this skill to attach files to `client.responses.create(...)` reliably.

## Preconditions

- Ensure `OPENAI_API_KEY` is available in the runtime environment.
- In a new Codex session, ask for outbound network approval before running API scripts:
- Whitelist domain: `api.openai.com`
- Methods: `POST` (create), `GET` (poll), `POST` (cancel)
- Reason text: `We will need this for Codex to natively run Python scripts that call OpenAI API in background mode.`
- Run API scripts with unbuffered output: `python -u ...`.
- Emit progress and error logs to stdout/stderr.

## Core Workflow

1. Upload file(s) with `client.files.create(...)`.
2. Build `input` content with `input_text` and attachment items:
- Document-style attachment: `{"type": "input_file", "file_id": "..."}`
- Image-style attachment: `{"type": "input_image", "image_file_id": "..."}`
3. Call `client.responses.create(...)`.
4. If background mode is enabled, poll with `client.responses.retrieve(response_id)`.
5. Delete uploaded files in `finally` unless retention is explicitly requested.

## Essential Code Blocks

### Attach a document file (`input_file`)

```python
from pathlib import Path
from openai import OpenAI

client = OpenAI()
pdf_path = Path("worksheet.pdf")
uploaded = None

try:
    with pdf_path.open("rb") as fh:
        uploaded = client.files.create(file=fh, purpose="user_data")

    response = client.responses.create(
        model="gpt-5.2",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Check all answers and list corrections."},
                    {"type": "input_file", "file_id": uploaded.id},
                ],
            }
        ],
    )
    print(response.output_text)
finally:
    if uploaded is not None:
        client.files.delete(uploaded.id)
```

### Attach an image file (`image_file_id`)

```python
from openai import OpenAI

client = OpenAI()
image_upload = None

try:
    with open("diagram.png", "rb") as fh:
        image_upload = client.files.create(file=fh, purpose="vision")

    response = client.responses.create(
        model="gpt-5.2",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Describe the geometry shown and produce LaTeX."},
                    {"type": "input_image", "image_file_id": image_upload.id},
                ],
            }
        ],
    )
    print(response.output_text)
finally:
    if image_upload is not None:
        client.files.delete(image_upload.id)
```

### Use background mode with file attachment and polling

```python
import time
from openai import OpenAI

client = OpenAI()
uploaded = None

try:
    with open("long_report.pdf", "rb") as fh:
        uploaded = client.files.create(file=fh, purpose="user_data")

    created = client.responses.create(
        model="gpt-5.2",
        background=True,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Perform a detailed audit and summarize issues."},
                    {"type": "input_file", "file_id": uploaded.id},
                ],
            }
        ],
    )
    response_id = created.id
    print(f"[submitted] response_id={response_id} status={getattr(created, 'status', 'unknown')}", flush=True)

    while True:
        latest = client.responses.retrieve(response_id)
        status = getattr(latest, "status", "unknown")
        print(f"[poll] response_id={response_id} status={status}", flush=True)
        if status in {"completed", "failed", "cancelled", "expired", "incomplete"}:
            break
        time.sleep(10)

    if status == "completed":
        print(latest.output_text)
    else:
        raise RuntimeError(f"Background response ended with status={status}")
finally:
    if uploaded is not None:
        client.files.delete(uploaded.id)
```

## Execution Rules

- Use the Responses API (`client.responses.create`, `client.responses.retrieve`), not Chat Completions.
- Include at least one `input_text` instruction alongside attached files.
- Use `purpose="user_data"` for document attachment and `purpose="vision"` for image attachment.
- Always track uploaded file IDs and clean them up unless user requirements say otherwise.
- Prefer explicit status logging for submit and poll phases.
- Run long API scripts as `python -u script.py ...` so logs stream in real time.

## Local Repository Examples

- `example_calling_api.py` demonstrates image upload plus `input_image` attachment.
- `pdf_to_latex/vision_transcriber.py` demonstrates PDF upload plus `input_file` attachment and cleanup.
