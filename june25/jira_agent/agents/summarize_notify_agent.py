from dotenv import load_dotenv
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain.chat_models.base import BaseChatModel
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from tools.email import individual_email_tool
from state import JiraAgentState


def get_agent(llm: BaseChatModel) -> CompiledStateGraph:
    """This method gets the summarize and notify agent
    """
    summarize_agent = create_react_agent(
        model=llm,
        tools=[individual_email_tool],
        prompt="",
        state_schema=JiraAgentState
    )
    return summarize_agent