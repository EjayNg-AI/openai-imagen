# Background API tasks

Code blocks and examples for background API tasks are attached below.

For background API tasks, they must use the Responses API. Older "chat.completions" endpoints cannot be used.

For background tasks, we must periodically poll the server to determine if the task has been completed or failed.

---

## Basic Structure of an API call using background mode

This is the basic structure of an API call which allows the model to run in a mode known as "background" mode. (See a more complete example in the next section.)

Here, we use the model `gpt-5-pro`. This model must be fixed. Only the coder / coding agent is allowed to update the model name manually. We do not leave this as a user-chosen option in the frontend web interface.

Furthermore, text verbosity and reasoning effort parameters cannot be specified for the `got-5-pro` model. Hence, the frontend web interface must not include options for the user to specify them.

The `store = True` parameter also cannot be specified for background API calls, unlike for other OpenAI models.

```python

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-5-pro",
  input=[],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={
    "summary": null
  },
  tools=[
    {
      "type": "web_search",
      "user_location": {
        "type": "approximate"
      },
      "search_context_size": "high"
    }
  ],
  background = True,
)

```

---

## A more complete example of an API call using background mode

A more complete example of an API call which employs background mode:

```python

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-5-pro",
  input=[
    {
      "role": "developer",
      "content": [
        {
          "type": "input_text",
          "text": "You are a creative and talented storyteller, as well as an experienced critique and connoisseur of literary works."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Give me a short critique of the lina trilogy and the afterword."
        },
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Overall\nThe Lina Trilogy is a rare thing: a near‑future narrative that’s both emotionally legible and technically literate. It understands parasociality as an industry; it reframes “alignment” as a human problem before it is a model problem; and it finds an ending that is neither Luddite retreat nor shiny inevitabilism."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Write a short offshoot to the lina trilogy."
        },
      ]
    },
  ],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={
    "summary": null
  },
  tools=[
    {
      "type": "web_search",
      "user_location": {
        "type": "approximate"
      },
      "search_context_size": "high"
    }
  ],
  background = True,
)

```

## Polling for a response

```python 

import time
import openai

client = openai.OpenAI()

# 1. Create background response
resp = client.responses.create(
    model="gpt-5-pro",
    input="Do a long, detailed analysis of the lina trilogy.",
    background=True,
)

response_id = resp.id
print("Started background job:", response_id)

# 2. Poll
while True:
    status_resp = client.responses.retrieve(response_id)
    status = status_resp.status

    if status in ("completed", "failed", "cancelled"):
        break

    time.sleep(61)  # backoff

if status_resp.status == "completed":
    print("Final output:")
    print(status_resp)
else:
    print("Job did not complete successfully:", status_resp.status)

```

---

## Model output

This is an example of a typical model output we expect. 

The assistant textual output is: "Offshoot: Witness Night\n\nThe first time Mara held the Shard box, it smelled like dust and aspirin.\n\nIt was a lunch‑cooler‑sized case with a rubber gasket and a red toggle under a transparent cap."

```python

{
  "background": true,
  "billing": {
    "payer": "developer"
  },
  "conversation": null,
  "created_at": 1765339742,
  "error": null,
  "id": "resp_0389930dd33170b8006938f25e984881909af1e929f2af0625",
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "metadata": {},
  "model": "gpt-5-pro-2025-10-06",
  "object": "response",
  "output": [
    {
      "content": null,
      "encrypted_content": null,
      "id": "rs_0389930dd33170b8006938f3e5f748819093bc11fc7628b108",
      "status": null,
      "summary": [],
      "type": "reasoning"
    },
    {
      "content": [
        {
          "annotations": [],
          "logprobs": [],
          "text": "Offshoot: Witness Night\n\nThe first time Mara held the Shard box, it smelled like dust and aspirin.\n\nIt was a lunch‑cooler‑sized case with a rubber gasket and a red toggle under a transparent cap.",
          "type": "output_text"
        }
      ],
      "id": "msg_0389930dd33170b8006938f3e5f89c8190844b4392708e436b",
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "prompt_cache_retention": null,
  "reasoning": {
    "effort": "high",
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "store": true,
  "temperature": 1,
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "tool_choice": "auto",
  "tools": [
    {
      "filters": null,
      "search_context_size": "high",
      "type": "web_search",
      "user_location": {
        "city": null,
        "country": null,
        "region": null,
        "timezone": null,
        "type": "approximate"
      }
    }
  ],
  "top_logprobs": 0,
  "top_p": 1,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 30988,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 8034,
    "output_tokens_details": {
      "reasoning_tokens": 2560
    },
    "total_tokens": 39022
  },
  "user": null
}

```



