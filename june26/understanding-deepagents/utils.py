"""
This module will have reusable utilities
"""

from langchain.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_model() -> BaseChatModel:
    """This model returns the llm
    """
    model = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        project=os.getenv('PROJECT_ID')
    )
    return model