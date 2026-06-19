import os
import base64
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

image_path = r"dataset/images/sample/case_001/img_1.jpg"

if not os.path.exists(image_path):
    print(f"Error: image not found at {image_path}")
    sys.exit(1)

with open(image_path, "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

try:
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one sentence."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }
        ]
    )
    sys.stdout.reconfigure(encoding='utf-8')
    print("Response:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API Error: {e}")
