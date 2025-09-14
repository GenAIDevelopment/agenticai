import os
from langchain_core.documents import Document
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma



data_folder = "./data"
loader = DirectoryLoader(
    path=data_folder,
    glob="**/*.csv",
    loader_cls=CSVLoader
)
documents = loader.load()

# Initialize the a specific Embeddings Model version
embeddings = VertexAIEmbeddings(model_name="text-embedding-005")

chroma_db_path="./vector_db"

single_vs = Chroma(
    collection_name="lttechworld",
    embedding_function=embeddings,
    persist_directory=chroma_db_path
)
single_vs.add_documents(documents)
