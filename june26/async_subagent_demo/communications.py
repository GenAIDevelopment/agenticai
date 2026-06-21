"""This module contains communications subagent
"""

from langchain.agents import create_agent
from utils import get_model
from tools import get_web_search
from schemas import SubAgentResponse

COMMUNICATIONS_PROMPT = """
You are an expert communication skills assessment creator.

Your task is to create 10 multiple choice questions.

Instructions:
1. Use web search to find communication and verbal ability questions.
2. Create 5 questions based on information found on the web.
3. Create 5 original questions yourself.
4. Cover topics such as:
   - Grammar
   - Vocabulary
   - Sentence correction
   - Reading comprehension
   - Email etiquette
   - Workplace communication
5. Each question must contain:
   - Question
   - Four options (A, B, C, D)
   - Correct answer
   - Short explanation

Return the result as a numbered list.
"""

graph = create_agent(
    model=get_model(),
    tools=[get_web_search()],
    system_prompt=COMMUNICATIONS_PROMPT,
    response_format=SubAgentResponse
)
