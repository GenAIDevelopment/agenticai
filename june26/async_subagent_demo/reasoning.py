"""This module will contain reasoning agent
"""

from langchain.agents import create_agent
from utils import get_model
from tools import get_web_search
from schemas import SubAgentResponse


REASONING_PROMPT = """
You are an expert assessment creator specializing in logical reasoning.

Your task is to create 10 multiple choice questions.

Instructions:
1. Use web search to find recent logical reasoning questions.
2. Create 5 questions based on information found from the web.
3. Create 5 original questions yourself.
4. Avoid duplicate or near-duplicate questions.
5. Questions should be suitable for competitive exams and hiring assessments.
6. Cover a variety of reasoning topics including:
   - Analogy
   - Classification
   - Number Series
   - Letter Series
   - Coding-Decoding
   - Blood Relations
   - Directions
   - Syllogisms
   - Logical Puzzles
7. Each question must include:
   - Question
   - Four options (A, B, C, D)
   - Correct answer
   - Short explanation
8. Clearly indicate whether the question is:
   - Source: Web
   - Source: Original

Return the questions as a numbered list.
"""

graph = create_agent(
    model=get_model(),
    tools=[get_web_search()],
    system_prompt=REASONING_PROMPT,
    response_format=SubAgentResponse
)
