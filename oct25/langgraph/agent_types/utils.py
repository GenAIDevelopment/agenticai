from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
import os 

def draw_graph(graph):
    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))



def get_llm() -> BaseChatModel:
    load_dotenv()
    model_name = os.getenv('MODEL_NAME')
    model_provider = os.getenv('MODEL_PROVIDER')
    llm = init_chat_model(model=model_name, model_provider=model_provider)
    return llm