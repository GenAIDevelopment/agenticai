from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

gemini_llm = init_chat_model(model="gpt-4o")

class SummaryState(MessagesState):
    summary: str


def answer(state: SummaryState) -> SummaryState:
    summary = state['summary']
    
    if summary.strip() == "":
        messages = state['messages']
    else:
        system_message = f"This is conversation of existing summary {summary}"
        messages = [SystemMessage(system_message)] + state['messages']
    state['messages'] = gemini_llm.invoke(messages)
    return state


from langchain_core.messages import RemoveMessage
def summarize(state: SummaryState) -> SummaryState:
    summary = state['summary']

    if summary.strip() == "":
        pass
    else:
        if len(state['messages']) >= 6:
            system_message = SystemMessage(f"Summarize the following messsages {state['messages']}")
            result_message = gemini_llm.invoke(system_message)
            state['summary'] = result_message.content
            deleted_messages = [RemoveMessage(id = m.id) for m in state['messages'][-2:]]
            state['messages'] = deleted_messages + result_message
    return state


from typing import Literal
def should_summarise(state: SummaryState) -> Literal["yes", "no"]:
    if len(state['messages']) >= 6:
        return "yes"
    else:
        return "no"
    

summarize_graph_builder = StateGraph(SummaryState)
summarize_graph_builder.add_node("conversation", answer)
summarize_graph_builder.add_node("summarize_conversation", summarize)
summarize_graph_builder.set_entry_point("conversation")
summarize_graph_builder.add_conditional_edges(
   "conversation",
   should_summarise,
   {
       "yes": "summarize_conversation",
       "no": END
   }
)
summary_graph = summarize_graph_builder.compile()