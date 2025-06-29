from typing import Optional
from langgraph.prebuilt.chat_agent_executor import AgentState

class JiraAgentState(AgentState):
    """This state will have Messages
    """
    raw_bugs: Optional[str]
    summary: Optional[str]
    email_ids: Optional[str]
