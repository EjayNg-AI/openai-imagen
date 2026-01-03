# Documentation

---

```python

JSON_SCHEMA = {
        "type": "object",
        "properties": {
            "paragraphs": {
                "type": "array",
                "description": f"An array containing 5 paragraphs, each ranging from 250 to 350 words.",
                "minItems": 5,
                "maxItems": 5,
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The content of the paragraph",
                            "minLength": 1250,
                            "maxLength": 2450,
                        }
                    },
                    "required": ["text"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["paragraphs"],
        "additionalProperties": False,
    }


response = client.responses.create(
        model="gpt-5.2",
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": developer_message,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_message,
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "paragraphs",
                "strict": True,
                "schema": JSON_SCHEMA,
            },
            "verbosity": "high",
        },
        reasoning={
            "effort": "high",
            "summary": None,
        },
        tools=[],
    )

```
