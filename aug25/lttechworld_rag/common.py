from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel





def get_single_collection_vector_store(chroma_db_path="./vector_db") -> VectorStoreRetriever:
    """Get single collection vector store

    Args:
        chroma_db_path (str, optional): _description_. Defaults to "./vector_db".

    Returns:
        VectorStoreRetriever: _description_
    """
    # Initialize the a specific Embeddings Model version
    embeddings = VertexAIEmbeddings(model_name="text-embedding-005")
    single_vs = Chroma(
        collection_name="lttechworld",
        embedding_function=embeddings,
        persist_directory=chroma_db_path
    )
    retriever = single_vs.as_retriever()
    return retriever


def load_llm() -> BaseChatModel:
    llm =  init_chat_model(
        "gemini-2.5-flash-lite",
        model_provider="google_vertexai"
    )
    return llm
