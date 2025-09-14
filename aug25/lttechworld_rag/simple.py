from typing import TypedDict, List
from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from common import get_single_collection_vector_store, load_llm
from langgraph.graph import StateGraph, START, END


rag_prompt = ChatPromptTemplate.from_template(
    """You are an helpful assistant from lttechworld, an electronics ecommerce company.
    Use the following context to anwer the user's question accurately and helpfully.

    Context:
    {context}

    Question: {question}

    Instructions:
    - Base your answer primarily on the provided context
    - If the context doesn't contain enough information, say so clearly
    - Be specific and helpful in your response
    - If recommending any products, mention specific names and key features

    Answer:
    """
)

class RAGState(TypedDict):
    """State of the RAG
    """
    question: str
    answer: str
    context: List[Document]



# Create a retrieve node
def retrieve(state: RAGState) -> RAGState:
    """retrieve node

    Args:
        state (RAGState): _description_

    Returns:
        RAGState: _description_
    """
    question = state['question']
    vector_store = get_single_collection_vector_store()
    retrieved_docs = vector_store.invoke(question)
    for index, doc in enumerate(retrieved_docs):
        source = doc.metadata.get('source', 'unknown')
        content = doc.page_content
        print(f"Doc {index} [{source}]: {content}")
        state['context'] = retrieved_docs
        return state

def generate(state: RAGState) -> RAGState:
    """_summary_

    Args:
        state (RAGState): _description_

    Returns:
        RAGState: _description_
    """
    question = state['question']
    context_docs = state['context']

    context_text = "\n\n".join([ f"Source {doc.metadata.get('source', 'unknown')}\n Content: {doc.page_content}" for doc in context_docs ])
    
    prompt_with_values = rag_prompt.invoke({
        "context": context_text,
        "question": question
    })
    llm = load_llm()
    response = llm.invoke(prompt_with_values)
    state['answer'] = response.content
    return state

# Build a RAG


graph_builder = StateGraph(RAGState)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.set_entry_point("retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.set_finish_point("generate")

rag_graph_simple = graph_builder.compile()
