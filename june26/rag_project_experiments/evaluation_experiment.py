"""
Evaluation
"""

from langchain_core.documents import Document
# sparse
from langchain_community.retrievers.bm25 import BM25Retriever
# Hybrid
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from utils import get_embeddings_from_gcp, get_model_from_gcp

from deepeval import evaluate
from deepeval.models import GeminiModel
from deepeval.metrics import (
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    AnswerRelevancyMetric
)
from deepeval.test_case import LLMTestCase
import os

load_dotenv()

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

def format_docs(retrieved_docs: list[Document]) -> str:
    return "\n\n".join(
        f"[Page {d.metadata.get('page','?')}] {d.page_content}" for d in retrieved_docs
    )

def build_rag_chain(retriever):
    prompt = ChatPromptTemplate.from_template(
        "Answer the question using ONLY the context below"
        "If the answer is not in the context, sya you don't know"
        "Cite the page. \n\n"
        "Context: {context}\n\n"
        "Question: {question}"
    )
    llm = get_model_from_gcp()
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def run_chain_and_build_cases(retriever, rag_chain, cases: list[dict]) -> list[LLMTestCase]:
    llm_test_cases = []
    for case in cases:
        question = case["question"]
        contexts = [d.page_content for d in retriever.invoke(question)]
        answer = rag_chain.invoke(question)
        print(f"\nQuestion: {question}\nAnswer: {answer}")
        llm_test_cases.append(
            LLMTestCase(
                input=question,
                actual_output=answer,
                expected_output=case["expected"],
                retrieval_context=contexts
            )
        )
    return llm_test_cases

def evaluate_chain(llm_test_cases: list[LLMTestCase]):
    judge = GeminiModel(
        model="gemini-2.5-flash-lite",
        use_vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        temperature=0
    )

    metrics = [
        ContextualPrecisionMetric(threshold=0.7, model=judge),
        ContextualRecallMetric(threshold=0.7, model=judge),
        FaithfulnessMetric(threshold=0.7, model=judge),
        AnswerRelevancyMetric(threshold=0.7, model=judge)
    ]
    return evaluate(test_cases=llm_test_cases, metrics=metrics)

def main():
    cases = [
        {
            "question": "What does it mean to split something into equal parts?",
            "expected": "A fraction is what you get when you divide something into equal parts."
        },
        {
            "question": "What formula does the Exercise 4.3 use?",
            "expected": "Exercise 4.3 uses the triangle area formula: half of the base times height"
        }

    ]
    documents = build_documents()
    dense_retriever = build_dense_retriever(documents)
    sparse_retriever = build_sparse_retriever(documents)
    retriever = build_hybrid_retriever(
        dense_retriever, sparse_retriever
    )
    rag_chain = build_rag_chain(retriever)
    llm_test_cases = run_chain_and_build_cases(retriever, rag_chain, cases)
    results = evaluate_chain(llm_test_cases)
    print("=" * 100)
    print("DeepEval Evaluation Results")
    print("=" * 100)

    for i, test_result in enumerate(results.test_results, start=1):
        print(f"\n{'='*100}")
        print(f"Test Case #{i}")
        print(f"{'='*100}")

        if test_result.name:
            print(f"Name      : {test_result.name}")

        if test_result.input:
            print(f"Question  : {test_result.input}")

        if test_result.actual_output:
            print(f"Answer    : {test_result.actual_output}")

        print("\nMetrics")
        print("-" * 100)

        for metric in test_result.metrics_data:
            status = "✅ PASS" if metric.success else "❌ FAIL"

            print(f"""
    Metric      : {metric.name}
    Score       : {metric.score:.3f}
    Threshold   : {metric.threshold}
    Status      : {status}
    Reason      : {metric.reason}
    Cost        : {metric.evaluation_cost}
    Latency     : {metric.evaluation_time:.2f}s
    """)


if __name__ == "__main__":
    main()