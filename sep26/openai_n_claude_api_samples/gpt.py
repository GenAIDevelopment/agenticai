from openai import OpenAI
from openai.types.responses import Response
from dotenv import load_dotenv
import os


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
    