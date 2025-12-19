# JSON output in making API calls

The following documents shows examples of how to elicit JSON output from an OpenAI language model when making API calls.

---

## Example 1

The following `JSON_SCHEMA` requires the model to output **one JSON object** with exactly one top-level key:

* **`paragraphs`**: an **array** with **4–7 items** (`minItems=4`, `maxItems=7`)

  * each item must be an **object** with exactly one required field:

    * **`text`**: a **string** with **1250–2450 characters** (`minLength`, `maxLength`)
  * `additionalProperties: false` (both at the paragraph-object level and the top level) means **no extra keys are allowed** anywhere.

The length constraints apply **per paragraph** (per `text` field), **not** to the whole response.

The API call is made to the **OpenAI Responses API** (`client.responses.create`) and telling it:

* `model="gpt-5.2"`: which model to use.
* `instructions=developer_message`: your developer/system instructions.
* `input=[...]`: the user message content (as structured “input_text”).
* `text.format = {"type":"json_schema", "strict": True, "schema": JSON_SCHEMA}`:

  * output must be **valid JSON** that **conforms exactly** to the schema,
  * and because `strict=True`, the model should not add extra fields or “helpful” text outside JSON.
* `text.verbosity="high"`: ask for more detailed writing (still constrained by the schema).
* `reasoning.effort="high"`: allocate more internal reasoning effort (doesn’t mean it will show reasoning text; it’s about how hard it thinks).

```python

import json
from openai import OpenAI

client = OpenAI()

JSON_SCHEMA = json.loads(
    """
    {
      "type": "object",
      "properties": {
        "paragraphs": {
          "type": "array",
          "description": "An array containing 4 to 7 paragraphs, each ranging from 250 to 350 words.",
          "minItems": 4,
          "maxItems": 7,
          "items": {
            "type": "object",
            "properties": {
              "text": {
                "type": "string",
                "description": "The content of the paragraph (plain text).",
                "minLength": 1250,
                "maxLength": 2450
              }
            },
            "required": ["text"],
            "additionalProperties": false
          }
        }
      },
      "required": ["paragraphs"],
      "additionalProperties": false
    }
    """
)

response = client.responses.create(
    model="gpt-5.2",  # or `gpt-5.2-pro`
    instructions = developer_message,  # developer_message is the system message in proper markdown format
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": user_message,  # user_message is the text message the user sends the model
                }
            ],
        },
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "Produce structured output",   # A descriptive name
            "strict": True,
            "schema": JSON_SCHEMA,
        },
        "verbosity": "high",  # can be "low", "medium" or "high" 
    },
    reasoning={
        "effort": "high",  # can be "none", "low", "medium", "high", or "xhigh" 
    },
)

```

In response, the model will return an output of the following form:

```
{
  "ok": true,
  "paragraphs": [
    "1. Title: Force-Field Promenade Deck with Velvet Sunbeds\nA wide recreation promenade on a deep-space starliner, ~260 years ahead: an exterior ... ... ",
    "2. Title: LCARS Quiet-Ops Skydeck Meditation Gallery\nA vast “skydeck” chamber on a luxury exploration cruiser, ~310 years ahead, where the outer hull retracts into a recessed frame and an invisible force-field plane holds atmosphere directly against open space. The edge is a perfect rectangle of nothingness, only visible via a thin prismatic shimmer when a floating incense-mist ribbon grazes it. This is a recreation zone: slow ... ... ",
  ],
  "response": {
    "background": false,
    "billing": {
      "payer": "openai"
    },
    "conversation": null,
    "created_at": 1766029698,
    "error": null,
    "id": "resp_0626743e41db2cc900694379823ab08196b8ef36b59ffe80c1",
    "incomplete_details": null,
    "instructions": "# SYSTEM INSTRUCTIONS (DEVELOPER MESSAGE) FOR IMAGE PROMPT GENERATION\n\nYou are an expert **image-prompt writer** for photoreal, cinematic scene generation.\n\n## Goal\n\n* Produce **5 distinct prompts** (numbered 1–5), each with a **short title**.\n* If **the number of required paragraphs ( 5 ) is at least 3**, include **Star Trek: TNG–style consoles/themes** (LCARS-like pastel ribbons, rounded modules, quiet ops aesthetic) ... ... ",
    "max_output_tokens": null,
    "max_tool_calls": null,
    "metadata": {},
    "model": "gpt-5.2-2025-12-11",
    "object": "response",
    "output": [
      {
        "content": null,
        "encrypted_content": null,
        "id": "rs_0626743e41db2cc90069437982ab948196b0960e073afc5e45",
        "status": null,
        "summary": [],
        "type": "reasoning"
      },
      {
        "content": [
          {
            "annotations": [],
            "logprobs": [],
            "text": "{\"paragraphs\":[
                {\"text\":\"1. Title: Force-Field Promenade Deck with Velvet Sunbeds\\nA wide recreation promenade on a deep-space starliner, ~260 years ahead: an exterior-facing “void terrace” carved into the ship’s midsection, fully open to vacuum yet held by an invisible force-field edge ... ... "},
                {\"text\":\"2. Title: LCARS Quiet-Ops Skydeck Meditation Gallery\\nA vast “skydeck” chamber on a luxury exploration cruiser, ~310 years ahead, where the outer hull retracts into a recessed frame and an invisible force-field plane holds atmosphere directly against open space. The edge is a perfect rectangle of nothingness, only visible via a thin prismatic shimmer when a floating incense-mist ribbon grazes it ... ... "},
                ]}",
            "type": "output_text"
          }
        ],
        "id": "msg_0626743e41db2cc9006943798c9b508196b852502365790d20",
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
        "description": null,
        "name": "paragraphs_5",
        "schema_": {
          "additionalProperties": false,
          "properties": {
            "paragraphs": {
              "description": "An array containing 5 paragraphs, each ranging from 250 to 350 words.",
              "items": {
                "additionalProperties": false,
                "properties": {
                  "text": {
                    "description": "The content of the paragraph (plain text).",
                    "maxLength": 2450,
                    "minLength": 1250,
                    "type": "string"
                  }
                },
                "required": [
                  "text"
                ],
                "type": "object"
              },
              "maxItems": 5,
              "minItems": 5,
              "type": "array"
            }
          },
          "required": [
            "paragraphs"
          ],
          "type": "object"
        },
        "strict": true,
        "type": "json_schema"
      },
      "verbosity": "high"
    },
    "tool_choice": "auto",
    "tools": [],
    "top_logprobs": 0,
    "top_p": 0.98,
    "truncation": "disabled",
    "usage": {
      "input_tokens": 2353,
      "input_tokens_details": {
        "cached_tokens": 0
      },
      "output_tokens": 2961,
      "output_tokens_details": {
        "reasoning_tokens": 678
      },
      "total_tokens": 5314
    },
    "user": null
  }
}
```

---

## A useful pattern to employ

If you want **both** human-friendly writing **and** easy validation, schemas often include:

* a **machine-checkable** field (`word_count`, `score`, `min/max cost`, `due_date`)
* plus a **free-text** field (`comments`, `justification`, `summary`)

That combination is where JSON output becomes really powerful: you get text that reads well *and* structure your code can reliably process.

---

## Example 2

This example involves a teacher grading a term paper (rubric + comments + letter grade + pass/fail)

```python
import json
from openai import OpenAI

client = OpenAI()

TEACHER_GRADE_SCHEMA = json.loads(
    """
    {
      "type": "object",
      "properties": {
        "student_id": { "type": "string" },
        "assignment_title": { "type": "string" },
        "overall_letter_grade": {
          "type": "string",
          "enum": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
        },
        "pass": { "type": "boolean" },
        "rubric": {
          "type": "array",
          "minItems": 3,
          "items": {
            "type": "object",
            "properties": {
              "criterion": { "type": "string" },
              "score": { "type": "number", "minimum": 0 },
              "max_score": { "type": "number", "minimum": 1 },
              "comments": { "type": "string" }
            },
            "required": ["criterion", "score", "max_score", "comments"],
            "additionalProperties": false
          }
        },
        "strengths": { "type": "array", "items": { "type": "string" } },
        "areas_to_improve": { "type": "array", "items": { "type": "string" } },
        "actionable_revision_plan": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "task": { "type": "string" },
              "why_it_matters": { "type": "string" },
              "how_to_fix": { "type": "string" }
            },
            "required": ["task", "why_it_matters", "how_to_fix"],
            "additionalProperties": false
          }
        }
      },
      "required": [
        "student_id",
        "assignment_title",
        "overall_letter_grade",
        "pass",
        "rubric"
      ],
      "additionalProperties": false
    }
    """
)

developer_message = (
    "You are an instructor grading a term paper. "
    "Return ONLY JSON that matches the provided schema. "
    "Be specific, constructive, and align rubric comments with scores."
)

user_message = """STUDENT_ID: S12345
TITLE: The Ethics of AI in Education
[Paste the full term paper here...]
"""

response = client.responses.create(
    model="gpt-5.2",  # or another Structured-Outputs-capable model
    instructions=developer_message,
    input=[
        {
            "role": "user",
            "content": [{"type": "input_text", "text": user_message}],
        }
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "term_paper_grading",
            "strict": True,
            "schema": TEACHER_GRADE_SCHEMA,
        },
        "verbosity": "high",
    },
    reasoning={"effort": "high"},
)

raw_json = response.output_text
grade = json.loads(raw_json)

print(grade["overall_letter_grade"], grade["pass"])

```

---

## Examples of ther JSON schema

Other examples of JSON schema are as follows.

### Business requisition request (items + purpose + estimated cost range + approvals)

```json
{
  "type": "object",
  "properties": {
    "request_id": { "type": "string" },
    "requestor": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "department": { "type": "string" },
        "email": { "type": "string" }
      },
      "required": ["name", "department", "email"],
      "additionalProperties": false
    },
    "items": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "item_type": { "type": "string" },
          "description": { "type": "string" },
          "quantity": { "type": "integer", "minimum": 1 },
          "purpose": { "type": "string" },
          "estimated_cost_range": {
            "type": "object",
            "properties": {
              "currency": { "type": "string", "enum": ["SGD", "USD", "EUR", "GBP", "JPY"] },
              "min": { "type": "number", "minimum": 0 },
              "max": { "type": "number", "minimum": 0 }
            },
            "required": ["currency", "min", "max"],
            "additionalProperties": false
          }
        },
        "required": ["item_type", "quantity", "purpose", "estimated_cost_range"],
        "additionalProperties": false
      }
    },
    "needed_by": { "type": "string", "description": "ISO date, e.g. 2026-01-15" },
    "budget_code": { "type": "string" },
    "urgency": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
    "approvals": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "role": { "type": "string" },
          "approver": { "type": "string" },
          "status": { "type": "string", "enum": ["pending", "approved", "rejected"] },
          "note": { "type": "string" }
        },
        "required": ["role", "status"],
        "additionalProperties": false
      }
    }
  },
  "required": ["request_id", "requestor", "items", "urgency"],
  "additionalProperties": false
}
```

### Meeting minutes extractor (decisions + action items)

```json
{
  "type": "object",
  "properties": {
    "meeting_title": { "type": "string" },
    "date": { "type": "string" },
    "attendees": { "type": "array", "items": { "type": "string" } },
    "summary": { "type": "string" },
    "decisions": { "type": "array", "items": { "type": "string" } },
    "action_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "owner": { "type": "string" },
          "task": { "type": "string" },
          "due_date": { "type": "string" },
          "status": { "type": "string", "enum": ["open", "in_progress", "done"] }
        },
        "required": ["owner", "task", "status"],
        "additionalProperties": false
      }
    },
    "risks": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["meeting_title", "summary", "action_items"],
  "additionalProperties": false
}
```

### Invoice / receipt extraction (for automation)

```json
{
  "type": "object",
  "properties": {
    "vendor": { "type": "string" },
    "invoice_number": { "type": "string" },
    "invoice_date": { "type": "string" },
    "currency": { "type": "string" },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "quantity": { "type": "number", "minimum": 0 },
          "unit_price": { "type": "number", "minimum": 0 },
          "total": { "type": "number", "minimum": 0 }
        },
        "required": ["description", "total"],
        "additionalProperties": false
      }
    },
    "subtotal": { "type": "number", "minimum": 0 },
    "tax": { "type": "number", "minimum": 0 },
    "total": { "type": "number", "minimum": 0 }
  },
  "required": ["vendor", "line_items", "total"],
  "additionalProperties": false
}
```

### Customer support triage (category + severity + recommended response)

```json
{
  "type": "object",
  "properties": {
    "ticket_id": { "type": "string" },
    "category": { "type": "string" },
    "severity": { "type": "string", "enum": ["sev4", "sev3", "sev2", "sev1"] },
    "sentiment": { "type": "string", "enum": ["negative", "neutral", "positive"] },
    "needs_human": { "type": "boolean" },
    "key_facts": { "type": "array", "items": { "type": "string" } },
    "recommended_reply": { "type": "string" },
    "next_actions": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["category", "severity", "needs_human", "recommended_reply"],
  "additionalProperties": false
}
```

### Code review report (issues per file, with severity)

```json
{
  "type": "object",
  "properties": {
    "summary": { "type": "string" },
    "overall_risk": { "type": "string", "enum": ["low", "medium", "high"] },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file_path": { "type": "string" },
          "line_start": { "type": "integer", "minimum": 1 },
          "line_end": { "type": "integer", "minimum": 1 },
          "severity": { "type": "string", "enum": ["nit", "minor", "major", "critical"] },
          "problem": { "type": "string" },
          "suggested_fix": { "type": "string" }
        },
        "required": ["file_path", "severity", "problem"],
        "additionalProperties": false
      }
    }
  },
  "required": ["summary", "overall_risk", "issues"],
  "additionalProperties": false
}
```

### Research paper metadata extraction (indexing / library ingestion)

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "authors": { "type": "array", "items": { "type": "string" } },
    "year": { "type": "integer", "minimum": 1800, "maximum": 2100 },
    "abstract": { "type": "string" },
    "keywords": { "type": "array", "items": { "type": "string" } },
    "claims": { "type": "array", "items": { "type": "string" } },
    "limitations": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["title", "authors", "abstract"],
  "additionalProperties": false
}
```

### Travel itinerary planner (structured schedule)

```json
{
  "type": "object",
  "properties": {
    "trip_title": { "type": "string" },
    "timezone": { "type": "string" },
    "days": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "date": { "type": "string" },
          "segments": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "start_time": { "type": "string" },
                "end_time": { "type": "string" },
                "activity": { "type": "string" },
                "location": { "type": "string" },
                "notes": { "type": "string" }
              },
              "required": ["activity"],
              "additionalProperties": false
            }
          }
        },
        "required": ["date", "segments"],
        "additionalProperties": false
      }
    }
  },
  "required": ["trip_title", "days"],
  "additionalProperties": false
}
```

---
