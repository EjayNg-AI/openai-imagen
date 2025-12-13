# Codeblocks for normal API requests

```python

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-5.1",
  input=[
    {
      "role": "developer",
      "content": [
        {
          "type": "input_text",
          "text": "Output all mathematical expressions in LaTex. For inline latex, use $....$. For equations, use $$.....$$. Do not use square brackets \\[ .... \\]. Assume that any LaTex you output will be compiled in an environment that has the library packages amsmath and amssymb installed."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Define prime numbers."
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "A prime number is a positive integer larger than 1 whose only positive divisors are 1 and itself. The first few prime numbers are $2, 3, 5, 7, ...$."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Is 16 a prime number?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "16 is not a prime number because it is divisible by 4, which is different from 1 and 16."
        }
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
    "effort": "high",  # can be `none`, `low`, `medium`, or `high`
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
  store=True,
)
```
