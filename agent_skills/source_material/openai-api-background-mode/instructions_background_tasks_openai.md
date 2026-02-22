# Background API tasks

Code blocks and examples for background API tasks are attached below.

For background API tasks, they must use the Responses API. Older "chat.completions" endpoints cannot be used.

For background tasks, we must periodically poll the server to determine if the task has been completed or failed.

---

## Basic Structure of an API call using background mode

This is the basic structure of an API call which allows the model to run in a mode known as "background" mode. (See a more complete example in the next section.)

NOTE: The `store = True` parameter cannot be specified for background API calls, unlike for other OpenAI models.

```python

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-5.2",  # model can be changed
  input=[],
  text={
    "format": {
      "type": "text"
    },
    "verbosity": "high"  # can be `low`, `medium`, or `high`
  },
  reasoning={
    "effort": "high",  # can be `none`, `low`, `medium`, `high` or `xhigh`
  },
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
  model="gpt-5.2",  # model can be changed
  input=[
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
    },
    "verbosity": "high"  # can be `low`, `medium`, or `high`
  },
  reasoning={
    "effort": "high",  # can be `none`, `low`, `medium`, `high`, `xhigh`
  },
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
    model="gpt-5.2-pro",
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

    time.sleep(10)  # backoff, usually we want **10 seconds**, but less than 90 seconds

if status_resp.status == "completed":
    print("Final output:")
    print(status_resp)
else:
    print("Job did not complete successfully:", status_resp.status)

```
