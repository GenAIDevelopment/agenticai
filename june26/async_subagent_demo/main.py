"""This module represents the main agent
"""

from utils import get_model
from deepagents import create_deep_agent, AsyncSubAgent
from deepagents.backends import FilesystemBackend

async_subagents = [
    AsyncSubAgent(
        name="reasoning",
        graph_id="reasoning",
        description="""
Searches for and creates logical reasoning and aptitude 
multiple choice questions. Covers topics such as
analogy, classification, coding-decoding, series,
blood relations, directions, syllogisms, puzzles, 
and logical reasoning.
"""
    ),
    AsyncSubAgent(
        name="programming",
        graph_id="programming",
        description="""
Searches for and creates basic programming multiple choice
questions covering Python, algorithms, data structures,
programming fundamentals, and logical coding concepts.
"""
    ),
    AsyncSubAgent(
        name="communications",
        graph_id="communications",
        description="""
Searches for and creates communication skills assessment 
questions covering grammar, vocabulary, reading comprehension,
business communication, and workplace communication.
"""

    )
]


SUPERVISOR_PROMPT = """
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
"""

backend = FilesystemBackend(
    root_dir="./agent_workspace",
    virtual_mode=True
)

model = get_model()

agent = create_deep_agent(
    model=model,
    subagents=async_subagents,
    system_prompt=SUPERVISOR_PROMPT,
    backend=backend,
)
