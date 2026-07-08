from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import get_embeddings_from_gcp, get_model_from_gcp
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def ingest(
        knowledge_base_data_dir="./simple_rag_knowledge_base",
        file_format_glob = "**/*.txt",
        persist_directory="./simple_rag_vs",
        collection_name="simple_rag_collection"):
    """This method will ingest the documents
       and creates the vector store
    """
    # 1. Load the documents
    loader = DirectoryLoader(
        path=knowledge_base_data_dir,
        glob=file_format_glob,
        loader_cls=TextLoader
    )
    docs = loader.load()
    print(f"loaded - {len(docs)} documents")

    # 2. Attach document level medatadata
    for doc in docs:
        filename = doc.metadata["source"].split("\\")[-1]
        doc.metadata["topic"] = filename.replace(".txt", "")

    # 3. split the documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(docs)

    # 4. create embeddings
    embedding_function = get_embeddings_from_gcp()

    # 5. create vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        collection_name=collection_name,
        persist_directory=persist_directory
    )

    print(f"Stored {vector_store._collection.count()} chunks in Chroma Vector database")
    print("Ingestion completed")


def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def ask(
        question,
        persist_directory="./simple_rag_vs",
        collection_name="simple_rag_collection"):
    # 1. Get vector store
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=get_embeddings_from_gcp()
    )
    # 2. Create retriever
    retriever = vector_store.as_retriever()

    # 3. create a rag_prompt
    rag_prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the provided context below. 
If the context doesnot contain enough information to answer say i dont know 
rather than guessing or using outside knowledge

Context:
{context}

Question: {input}
                                                  
Answer: """)
    
    llm = get_model_from_gcp()

    # 4. retrieve docs
    retrieved_docs = retriever.invoke(question)
    context = format_docs(retrieved_docs)

    # 5. create chain
    chain =  rag_prompt | llm | StrOutputParser()

    answer = chain.invoke({"context": context, "input": question})

    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Response from vector store: {context}")







if __name__ == "__main__":
    #ingest()
    question = input("Enter your question: ")
    ask(question)