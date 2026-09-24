from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv
import os

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



def ask_gpt(question:str):
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=question
    )
    process_response(response)

def process_response(response: Response):
    print(f"Output From model: {response.output[-1].content[-1].text}")
    print(f"Input Tokens: {response.usage.input_tokens}")
    print(f"Output Tokens: {response.usage.output_tokens}")

def interact_with_model():
    ask_gpt("What is capital of France?")


def ask_gpt_to_do_something():
    load_dotenv()

    tools_definition = [{
        "type": "function",
        "name": "get_weather",
        "description": (
            "Retrieves the current weather temperature, forecast, "
            "and climate details for a specified city."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": (
                        "The name of the city to look up weather data for."
                    )
                }
            },
            "required": ["city"],
            "additionalProperties": False
        },
        "strict": True
    }]

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.responses.create(
        model="gpt-5.6-luna",
        input="Do I need to carry an umbrella to work in Hyderabad?",
        tools=tools_definition
    )

    print(response)    