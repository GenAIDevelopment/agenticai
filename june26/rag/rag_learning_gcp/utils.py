from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_model_from_gcp(model_name:str = "gemini-2.5-flash-lite") -> ChatGoogleGenerativeAI:
    """This method returns a chat model from gcp

    Args:
        model_name (str, optional): _description_. Defaults to "gemini-3.1-flash-lite".
    """
    return ChatGoogleGenerativeAI(
        model=model_name,
        )