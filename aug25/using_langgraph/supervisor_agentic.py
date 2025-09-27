from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Optional, TypedDict, Literal

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.output_parsers import StrOutputParser

embedding = VertexAIEmbeddings(model_name="text-embedding-005")
VECTOR_STORE = Chroma(persist_directory="vector_store", embedding_function=embedding)
retriever = VECTOR_STORE.as_retriever()
llm = init_chat_model("gemini-2.5-flash", model_provider="google_vertexai")
tavily_tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)


class GraphState(TypedDict):
    question: str
    docs: List[dict]
    draft: Optional[str]
    need_browse: bool
    citations: List[str]
    web_snippets: List[str]


SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a planner that decides tools. "
        "Given the user question, answer by one word"
        "'retrieve' if local knowledge likely suffices, 'browse' if web is needed; "
        "'hybrid' if both are useful, Prefer 'retrive' unless clearly time-sensitive or out-of-scope"
    ),
    (
        "human", 
        "Question {question}"
    )
])


def supervisor(state: GraphState) -> GraphState:
    plan =  (SUPERVISOR_PROMPT | llm | StrOutputParser()).invoke({"question": state['question']}).strip().lower()
    need_browse = plan in ('browse', 'hybrid')
    state["need_browse"] = need_browse
    return state


def retrieve(state: GraphState) -> GraphState:
    docs = retriever.get_relevant_documents(state['question'])
    state['docs'] = [{"page_content": doc.page_content, "metadata": dict(doc.metadata) }  for doc in docs ]
    return state

GRADE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict relevance grader for Retrieval"
        "say 'keep', if the chunk is direcly useful to answer the question; otherwise 'drop'. Be conservation"),
    (
        "human",
        "Question: {question} \n\nChunk: \n {chunk}\n")
])

def grade_documents(state: GraphState) -> GraphState:
    filtered = []
    for document in state["docs"]:
        verdict = (GRADE_PROMPT | llm | StrOutputParser()).invoke(
            {'question': state['question'],
            "chunk": document['page_content'] }).strip().lower()
        if "keep" in verdict:
            filtered.append(document)
    state["docs"] = filtered
    return state


def web_search(state: GraphState) -> GraphState:
    if not state["need_browse"]:
        return state
    snippets = []
    response = tavily_tool.invoke({"query": state["question"]})
    for item in response.get("results", []):
        title = item.get('title', '')
        url = item.get('url', '')
        content = (item.get('content', ''))[:600]
        snippets.append(f"{title}\n{url}\n{content}")
    state['web_snippets'] = snippets
    return state


ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are an expert who answers only using the provided context"
        "If the context is thin, explain limits and ask a targetted follow-up"
    ),
    (
        "human",
        "User question: \n{question}\n\n"
        "Local context (top chunks):\n{docs}\n\n"
        "Web context (optional): \n{web}\n"

    )
])


def answer(state: GraphState) -> GraphState:
    docs_txt = "\n\n-----\n\n".join([document['page_content'] for document in state["docs"]])
    snippets = state.get('web_snippets', [])
    if len(snippets) > 0:
        webs_txt = "\n\n-----\n\n".join(state["web_snippets"]) if state["web_snippets"] else "N/A"
    else:
        webs_txt = "N/A"
    draft = (ANSWER_PROMPT | llm | StrOutputParser()).invoke({
        "question": state["question"],
        "docs": docs_txt,
        "web": webs_txt
    })
    state["draft"] = draft
    return state


builder = StateGraph(GraphState)
builder.add_node("supervisor", supervisor)
builder.add_node("retrieve", retrieve)
builder.add_node("grade", grade_documents)
builder.add_node("web", web_search)
builder.add_node("answer", answer)

builder.set_entry_point("supervisor")
builder.add_edge("supervisor", "retrieve")
builder.add_edge("retrieve", "grade")

def need_browsing_after_grade(state: GraphState) -> Literal["web", "answer"]:
    return "web" if state.get("need_browse") else "answer"

builder.add_conditional_edges(
    "grade", need_browsing_after_grade, {"web": "web", "answer": "answer"}
)
builder.add_edge("web", "answer")
builder.add_edge("answer", END)
graph = builder.compile()

if __name__ == "__main__":
    pass
