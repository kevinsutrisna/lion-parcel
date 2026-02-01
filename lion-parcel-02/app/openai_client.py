import base64
import os
from openai import OpenAI

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "openai/gpt-4o-mini"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=GITHUB_TOKEN,
)


def describe_image(image_bytes: bytes) -> str:
    b64 = base64.standard_b64encode(image_bytes).decode("ascii")
    data_url = f"data:image/jpeg;base64,{b64}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that describes images in details.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in one sentence."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url,
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
    )

    return response.choices[0].message.content
