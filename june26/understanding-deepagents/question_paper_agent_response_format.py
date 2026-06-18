from utils import get_model
from deepagents.backends import FilesystemBackend
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from deepagents import create_deep_agent
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

class MultipleChoiceQuestion(BaseModel):
    question: str = Field(description="Question")
    A: str = Field(description="Choice A")
    B: str = Field(description="Choice B")
    C: str = Field(description="Choice C")
    D: str = Field(description="Choice D")

    answer: Literal["A", "B", "C", "D"] = Field(
        description="Correct answer"
    )

    explanation: str = Field(description="Explanation to answer")

class SubAgentResponse(BaseModel):
    mcqs: list[MultipleChoiceQuestion] = Field(
        min_length=1,
        description="List of MCQs"
    )
    topic: str = Field(
        min_length=1,
        description="Topic name"
    )

model = get_model()
backend = FilesystemBackend(
    root_dir="./question_paper_workspace",
    virtual_mode=True)

web_search = TavilySearch(
    max_results=10,
    topic="general"
)

reasoning_subagent = {
    "name": "reasoning_subagent",
    "description": (
        "Searches for and creates logical reasoning and aptitude "
        "multiple choice questions. Covers topics such as "
        "analogy, classification, coding-decoding, series, "
        "blood relations, directions, syllogisms, puzzles, "
        "and logical reasoning."
    ),
    "system_prompt": """
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
""",
    "tools": [web_search],
    "response_format": SubAgentResponse
}

programming_subagent = {
    "name": "programming_subagent",
    "description": (
        "Searches for and creates basic programming multiple choice "
        "questions covering Python, algorithms, data structures, "
        "programming fundamentals, and logical coding concepts."
    ),
    "system_prompt": """
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
""",
    "tools": [web_search],
    "response_format": SubAgentResponse
}


communication_subagent = {
    "name": "communication_subagent",
    "description": (
        "Searches for and creates communication skills assessment "
        "questions covering grammar, vocabulary, reading comprehension, "
        "business communication, and workplace communication."
    ),
    "system_prompt": """
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
""",
    "tools": [web_search],
    "response_format": SubAgentResponse
}


agent = create_deep_agent(
    model=model,
    backend=backend,
    subagents=[communication_subagent, reasoning_subagent, programming_subagent],  
    system_prompt="""
You are responsible for creating 30 multiple choice questions on
reasoning
programming
communications

You have access to subagents, where you can delegate the work
Ensure you create todos first and store in /todos.md
Capture the response from every subagent and save in /<topic>.json

Store the final question paper in /questions.md where for every question we have 4 choices
Store the final answers in /answers.md
Store the final explanations in /explanations.md

Ensure you crosschekc the questions, answers and explanations before writing to filesystem

Ensure the final output is in standard markdown format.
""",

)


if __name__ == "__main__":
    result = agent.invoke(
        input={
            "messages": [
                {
                    "role": "user",
                    "content": "I need 30 questions with 10 each on reasoning, basic programming and communications for an entry level job in a software startup"
                }
            ]
        }
    )
    print(result["messages"][-1].content)
