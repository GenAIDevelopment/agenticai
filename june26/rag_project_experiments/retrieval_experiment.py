"""
Dense vs Sparse vs Hybrid Retrieval
"""

from langchain_core.documents import Document
# sparse
from langchain_community.retrievers.bm25 import BM25Retriever
# Hybrid
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from dotenv import load_dotenv
from utils import get_embeddings_from_gcp

def build_documents() -> list[Document]:
    raw_chunks = [
        {
            "text": "A fraction represents a part of a whole. When we divide"
            "a pizza into 4 equal slices and take 1, we have 1/4 of the pizza.",
            "metadata": {"chapter": "Fractions", "page": 12},
        },
        {
            "text": "Dividing a cake into equal portions and taking one part"
            "is the same idea as a fraction.",
            "metadata": {"chapter": "Fractions", "page": 13},
        },
        {
            "text": "Photosynthesis is the process by which plants convert "
            "sunlight into chemical energy.",
            "metadata": {"chapter": "Biology", "page": 45},
        },
        {
            "text": "Exercise 4.3 asks students to calculate area of a "
            "triangle using the formula half base times height.",
            "metadata": {"chapter": "Geometry", "page": 88},
        }

    ]
    return [Document(page_content=chunk["text"], metadata=chunk["metadata"])
            for chunk in raw_chunks]


# Dense retriever

def build_dense_retriever(documents: list[Document]) -> VectorStoreRetriever:
    embedding_model = get_embeddings_from_gcp()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name="retriever_demo"
    )

    dense_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )
    return dense_retriever

# sparse retriever

def build_sparse_retriever(documents: list[Document]) -> BM25Retriever:
    sparse_retriever = BM25Retriever.from_documents(documents)
    sparse_retriever.k = 2
    return sparse_retriever

def build_hybrid_retriever(dense_retriever, sparse_retriever) -> EnsembleRetriever:
    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, sparse_retriever],
        weights=[0.5, 0.5]
    )
    return hybrid_retriever

def run_comparision():
    documents = build_documents()
    dense_retriever = build_dense_retriever(documents)
    sparse_retriever = build_sparse_retriever(documents)
    hybrid_retriever = build_hybrid_retriever(dense_retriever, sparse_retriever)

    queries = [
        "What does it mean to split something into equal portions",
        "Exercise 4.3 triangle area formula"

    ]

    for query in queries:
        print(f"\n{'=' * 60}\nQuery: {query}\n{'=' * 60}")

        print("\n--- DENSE (semantic) ----")
        for doc in dense_retriever.invoke(query):
            print(f"{doc.page_content}")

        print("\n--- SPARSE (keyword) ----")
        for doc in sparse_retriever.invoke(query):
            print(f"{doc.page_content}")

        print("\n--- HYBRID (fused via RRF) ---")
        for doc in hybrid_retriever.invoke(query):
            print(f"{doc.page_content}")

if __name__ == "__main__":
    run_comparision()

