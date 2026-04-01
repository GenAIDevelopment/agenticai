"""This module will contain
basic interaction with a gcp vertex model
"""

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()
project = os.getenv('GOOGLE_CLOUD_PROJECT')


# model
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    vertexai = True,
    project = project
)

country = input("Enter the country of your choice? ")

# lets create messages
messages = [
    SystemMessage("You are social teacher for a Primary School, Explain interestic facts also"),
    HumanMessage(f"What is capital of {country}?")
]

response = llm.invoke(messages)
print(response.content)

