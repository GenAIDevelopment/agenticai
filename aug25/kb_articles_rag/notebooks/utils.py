from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import Chroma


def get_vertex_ai_model(model: str = "gemini-2.5-flash-lite") -> BaseChatModel:
    """This method returns the vertex ai model

    Args:
        model (str, optional): model Name. Defaults to "gemini-2.5-flash-lite".

    Returns:
        BaseChatModel: chat model instance
    """
    return init_chat_model(model=model, model_provider="google_vertexai")


def get_vertex_ai_embedding(model_name: str = "text-embedding-005") -> VertexAIEmbeddings:
    """Get the vertex ai embedding

    Args:
        model_name (str, optional): name of the embedding model. Defaults to "text-embedding-005".

    Returns:
        VertexAIEmbeddings: vertexai embedding object
    """
    return VertexAIEmbeddings(model_name=model_name)


def get_fixed_size_chunker(chunk_size=500, chunk_overlap=50, seperator="\n") -> CharacterTextSplitter:
    """Fixed Size Chunker

    Args:
        chunk_size (int, optional): _description_. Defaults to 500.
        chunk_overlap (int, optional): _description_. Defaults to 50.
        seperator (str, optional): _description_. Defaults to "\n".

    Returns:
        CharacterTextSplitter: _description_
    """

    return CharacterTextSplitter(
        separator=seperator,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )


def get_recursive_chunker(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n", "\n\n", "\n##", ".", ",", " "]) -> RecursiveCharacterTextSplitter:
    """Get Recursive chunker

    Args:
        chunk_size (int, optional): _description_. Defaults to 500.
        chunk_overlap (int, optional): _description_. Defaults to 50.
        separators (list, optional): _description_. Defaults to ["\n", "\n\n", "\n##", ".", ",", " "].

    Returns:
        RecursiveCharacterTextSplitter: _description_
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )


def get_semantic_chunker(
        embedding: Embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=95) -> SemanticChunker:
    """Get Semantic chunker

    Args:
        embedding (Embeddings): _description_
        breakpoint_threshold_type (str, optional): _description_. Defaults to "percentile".
        breakpoint_threshold_amount (int, optional): _description_. Defaults to 95.

    Returns:
        SemanticChunker: _description_
    """
    return SemanticChunker(
        embeddings=embedding,
        breakpoint_threshold_amount=breakpoint_threshold_amount,
        breakpoint_threshold_type=breakpoint_threshold_type
    )


def vector_store_from_chunks(
        chunks,
        embedding,
        name,
        persist_directory="./vectordb") -> Chroma:
    """Get Vector store

    Args:
        chunks (_type_): _description_
        embedding (_type_): _description_
        name (_type_): _description_
        persist_directory (_type_): _description_

    Returns:
        Chroma: _description_
    """
    return Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        collection_name=name,
        persist_directory=persist_directory
    )
