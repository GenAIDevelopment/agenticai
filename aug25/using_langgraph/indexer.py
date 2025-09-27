from langchain_community.vectorstores import Chroma
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader # Or use the appropriate loader for your file type
from dotenv import load_dotenv
import pathlib, sys




# Define the path to your directory
directory_path = "data" 

# Create a DirectoryLoader instance
# The 'glob' parameter with "**/*.txt" ensures recursive search for all .txt files
# loader_cls specifies the loader to use for the files found
loader = DirectoryLoader(
    directory_path,
    glob="**/*.txt",  # Recursive search for all .txt files
    loader_cls=TextLoader,
    recursive=True # Ensure recursive behavior
)

# Load the documents
documents = loader.load()

spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = spliter.split_documents(documents)
embedding = VertexAIEmbeddings(model_name="text-embedding-005")
Chroma.from_documents(chunks,embedding,persist_directory="vector_store")
print(f"Indexed {len(chunks)} into ./vector_store")
