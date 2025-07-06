"""
This module has summary react agent
"""

from langchain.chat_models.base import BaseChatModel
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from tools.email import individual_email_tool
from common.state import JiraAgentState
from langchain_core.messages import SystemMessage


def get_agent(llm: BaseChatModel) -> CompiledStateGraph:
    """This agent summarizes the information passed and notifies via email

    Args:
        llm (BaseChatModel): model

    Returns:
        CompiledStateGraph: graph
    """
    summarize_agent = create_react_agent(
        name="summarize_agent",
        model=llm,
        tools=[individual_email_tool],
        prompt=SystemMessage(content=
        "you are an Summarize agent, responsible for summarizing the information recieved, use all@qt.com as email id and summary as message, subject should be summary of defects and call the email tool to notify"),
        #state_schema=JiraAgentState
    )
    return summarize_agent
