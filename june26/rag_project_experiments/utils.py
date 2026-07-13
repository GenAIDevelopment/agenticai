from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import base64

load_dotenv()

def get_model_from_gcp(model_name:str = "gemini-2.5-flash-lite") -> ChatGoogleGenerativeAI:
    """This method returns a chat model from gcp

    Args:
        model_name (str, optional): _description_. Defaults to "gemini-3.1-flash-lite".
    """
    return ChatGoogleGenerativeAI(
        model=model_name,
        )

def get_embeddings_from_gcp(model_name:str = "text-embedding-005") -> GoogleGenerativeAIEmbeddings:
    """This method returns a chat model from gcp

    Args:
        model_name (str, optional): _description_. Defaults to "text-embedding-005.
    """
    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        )

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()