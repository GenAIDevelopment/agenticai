"""
This module will have functions, variables to get the llm
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel

async def get_llm() -> BaseChatModel:
    """This method gets the llm
    """
    load_dotenv()
    llm = init_chat_model(
        model=os.getenv('MODEL_ID'),
        model_provider=os.getenv('MODEL_PROVIDER')
    )
    return llm
