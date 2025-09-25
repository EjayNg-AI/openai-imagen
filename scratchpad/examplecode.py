import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment")

client = OpenAI(api_key=api_key)


def create_story_response():
    return client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Be concise",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Write 5 different paragraphs each containing a very short story. Two of the five paragraphs must be about office workers.",
                    }
                ],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "five_paragraphs",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "paragraphs": {
                            "type": "array",
                            "description": "An array containing five paragraphs, each ranging from 150 to 200 words.",
                            "minItems": 5,
                            "maxItems": 5,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "The content of the paragraph (plain text).",
                                        "minLength": 800,
                                        "maxLength": 1300,
                                    }
                                },
                                "required": ["text"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["paragraphs"],
                    "additionalProperties": False,
                },
            },
            "verbosity": "medium",
        },
        reasoning={
            "effort": "medium",
            "summary": "auto",
        },
        tools=[],
        store=True,
        include=[
            "reasoning.encrypted_content",
            "web_search_call.action.sources",
        ],
    )


response = create_story_response()
