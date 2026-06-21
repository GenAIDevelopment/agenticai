"""This module contains programming subagent
"""

from langchain.agents import create_agent
from utils import get_model
from tools import get_web_search
from schemas import SubAgentResponse

PROGRAMMING_PROMPT = """
You are an expert programming assessment creator.

Your task is to create 10 multiple choice questions.

Instructions:
1. Use web search to find recent programming interview and aptitude questions.
2. Create 5 questions based on information found on the web.
3. Create 5 original questions yourself.
4. Questions should be beginner-friendly.
5. Cover topics such as:
   - Variables and data types
   - Loops and conditions
   - Functions
   - Lists and dictionaries
   - Basic algorithms
   - Programming logic
6. Each question must contain:
   - Question
   - Four options (A, B, C, D)
   - Correct answer
   - Short explanation

Return the result as a numbered list.
"""

graph = create_agent(
    model = get_model(),
    tools = [get_web_search()],
    system_prompt = PROGRAMMING_PROMPT,
    response_format = SubAgentResponse
)