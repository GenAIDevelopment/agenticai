"""This module has agent to fetch jira defects
"""

from dotenv import load_dotenv
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain.chat_models.base import BaseChatModel
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from common.state import JiraAgentState
from langchain_core.messages import SystemMessage


def get_agent(llm: BaseChatModel) -> CompiledStateGraph:
    """This agent is used to communicate with jira and get the information

    Args:
        llm (BaseChatModel): model

    Returns:
        CompiledStateGraph: graph
    """
    load_dotenv()
    jira = JiraAPIWrapper()
    toolkit = JiraToolkit.from_jira_api_wrapper(jira)
    jira_tools = toolkit.get_tools()
    jira_agent = create_react_agent(
        name="jira_agent",
        model=llm,
        tools=jira_tools,
        prompt=SystemMessage(content="You are an Jira assistant, responsible in project management activities using jira tools to fetch information from jira projects"),
        #state_schema=JiraAgentState,
    )
    return jira_agent
