import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel

def get_llm() -> BaseChatModel:
    """This method gets the llm
    """
    load_dotenv()
    llm = init_chat_model(
        os.getenv('MODEL_ID'),
        os.getenv('MODEL_PROVIDER')
    )
    return llm
