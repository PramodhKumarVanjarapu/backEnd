import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def evaluate_assignment(prompt: str) -> str:
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=3000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    # Some SDKs may return structured content; normalize to string
    if isinstance(content, str):
        return content

    return json.dumps(content)