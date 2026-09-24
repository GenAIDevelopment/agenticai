from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv
import os

def ask_claude(question: str):
    load_dotenv()
    client = Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
    )
    response = client.messages.create(
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": question
        }],
        model="claude-haiku-4-5"
    )
    process_response(response)

def process_response(response: Message):
    print(f"Output From model: {response.content[-1].text}")
    print(f"Input Tokens: {response.usage.input_tokens}")
    print(f"Output Tokens: {response.usage.output_tokens}")


def interact_with_model():
    ask_claude("What is captial of France?")