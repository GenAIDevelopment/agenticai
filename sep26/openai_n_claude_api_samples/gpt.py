from openai import OpenAI
from dotenv import load_dotenv
import os


def interact_with_model():
    load_dotenv()
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY')
    )
    response = client.responses.create(
        model="gpt-5.6-luna",
        input="What is capital of France?"
    )
    print(response)
    