from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

class MathTeacherState(TypedDict):
    query: str
    detailed_explanation: bool
    result: str


load_dotenv()
model_name = os.getenv('MODEL_NAME')
model_provider = os.getenv('MODEL_PROVIDER')
llm = init_chat_model(model=model_name, model_provider=model_provider)


def give_me_result(state: MathTeacherState) -> MathTeacherState:
    """Directly getting result

    Args:
        state (MathTeacherState): _description_

    Returns:
        MathTeacherState: _description_
    """
    PROMPT = f"You are a mathematician, Give me result directly of the math problem {state['query']}. No explanation required"
    state['result'] = llm.invoke(PROMPT)
    return state

def give_me_explanation(state: MathTeacherState) -> MathTeacherState:
    """getting result with explanation

    Args:
        state (MathTeacherState): _description_

    Returns:
        MathTeacherState: _description_
    """
    PROMPT = f"You are a mathematician, Explain step by step on how to solve problem {state['query']}."
    state['result'] = llm.invoke(PROMPT)
    return state

def next_node(state: MathTeacherState) -> Literal['responder', 'explainer']:
    if state['detailed_explanation'] == True:
        return 'explainer'
    return 'responder'

math_solver_graph = StateGraph(MathTeacherState)
math_solver_graph.add_node("responder", give_me_result)
math_solver_graph.add_node("explainer", give_me_explanation)
math_solver_graph.add_conditional_edges(
    START,
    next_node
)
math_solver_graph.add_edge('responder', END)
math_solver_graph.add_edge('explainer', END)
graph = math_solver_graph.compile()
