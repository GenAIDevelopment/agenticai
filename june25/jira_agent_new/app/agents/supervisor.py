"""This module creates a supervisor agent
"""

from langgraph_supervisor import create_supervisor
from langgraph.graph.state import CompiledStateGraph
from langchain.chat_models.base import BaseChatModel
from app.agents.fetch import get_agent as jira_agent
from app.agents.summarize import get_agent as summarize_agent
from langchain_core.messages import SystemMessage
from app.common.state import JiraAgentState



async def get_supervisor(llm: BaseChatModel) -> CompiledStateGraph:
    """This function creates a supervisor agent

    Args:
        llm (BaseChatModel): llm used 

    Returns:
        CompiledStateGraph: graph
    """
    supervisor_graph_builder = create_supervisor(

        model=llm,
        agents=[await jira_agent(llm=llm), await summarize_agent(llm=llm)],
        prompt=SystemMessage(content=
            "You are a supervisor managing two agents \n" +
            " - 'jira_agent': Get all defects in Learning Management System Project \n" +
            " - 'summarize_agent':  Summarize the defects recieved \n" +
            "Assign work to one agent at a time, do not call agents in parallel \n" +
            "Do not work yourself"
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
        #state_schema=JiraAgentState
    ).compile()
    #supervisor_graph = supervisor_graph_builder.compile()
    return supervisor_graph_builder
