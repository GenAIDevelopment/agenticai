from dotenv import load_dotenv
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langchain.chat_models.base import BaseChatModel
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from state import JiraAgentState

def get_agent(llm: BaseChatModel) -> CompiledStateGraph:
    """This method gets the defects_agent
    """
    load_dotenv()
    jira = JiraAPIWrapper()
    toolkit = JiraToolkit.from_jira_api_wrapper(jira)
    jira_tools = toolkit.get_tools()
    jira_agent = create_react_agent(model=llm,
                   tools=jira_tools,
                   prompt="You are an helpful assistant in project management activities",
                   state_schema=JiraAgentState
                   )
    return jira_agent

