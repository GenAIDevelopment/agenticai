from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

def get_vertex_ai_model(model:str="gemini-2.5-flash-lite") -> BaseChatModel:
    """This method returns the vertex ai model

    Args:
        model (str, optional): model Name. Defaults to "gemini-2.5-flash-lite".

    Returns:
        BaseChatModel: chat model instance
    """
    return init_chat_model(model=model, model_provider="google_vertexai")
