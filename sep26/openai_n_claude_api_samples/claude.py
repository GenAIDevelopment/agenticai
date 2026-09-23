from anthropic import Anthropic
from dotenv import load_dotenv
import os

def interact_with_model():
    load_dotenv()
    client = Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
    )
    response = client.messages.create(
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "What is captial of France?"
        }],
        model="claude-haiku-4-5"
    )
    print(response)