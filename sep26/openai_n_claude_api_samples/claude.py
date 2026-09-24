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


def get_weather(city: str) -> dict:
    fake_weather_db = {
        'hyderabad': {
            'temp': '25',
            'forecast': 'Flash flood risk',
            'other_details': 'mostly cloudy'

        },
        'bangalore': {
            'temp': '33',
            'forecast': 'sunny',
            'other_details': 'clear sky'
        }
    }
    return fake_weather_db.get(city)

def ask_claude_to_do_something():
    load_dotenv()
    client = Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY'),
    )
    tools_definition = [{
        "name": "get_weather",
        "description": "Retrieves the current temperature, weather forecast, and climate details for a specified city.",
        "input_schema": {
            "type": "object",
            "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city to look up the weather for, e.g., 'hyderabad' or 'bangalore'."
            }
            },
            "required": ["city"]
        }
    }]
    messages = [
        {
            "role": "user", 
            "content": "Do i need to carry umbrella for work in hyderabad?"}
    ]
    response = client.messages.create(
        max_tokens=100,
        messages=messages,
        model="claude-haiku-4-5",
        tools=tools_definition
    )
    #process_response(response)
    print(response)