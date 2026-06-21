"""This module represents the main agent
"""

from utils import get_model
from deepagents import create_deep_agent, AsyncSubAgent
from deepagents.backends import (
    StoreBackend,
    FilesystemBackend,
    CompositeBackend,
    StateBackend
)
from context import Context


def make_backend(runtime):
    return CompositeBackend(
        default=StateBackend(runtime=runtime),
        routes={
            "/memories": StoreBackend(),
            "/exams": FilesystemBackend(
                root_dir="./agent_workspace",
                virtual_mode=True
            )
        }

    )


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
Ensure you create todos first and store in /exams/todos.md
Capture the response from every subagent and save in /exams/<topic>.json

Store the final question paper in /exams/questions.md where for every question we have 4 choices
Store the final answers in /exams/answers.md
Store the final explanations in /exams/explanations.md

Ensure you crosscheck the questions, answers and explanations before writing to filesystem

Ensure the final output is in standard markdown format.
"""


model = get_model()

agent = create_deep_agent(
    model=model,
    subagents=async_subagents,
    system_prompt=SUPERVISOR_PROMPT,
    backend=make_backend,
    memory=["./AGENTS.md"],
    context_schema=Context
)


if __name__ == "__main__":
    import asyncio

    async def main():
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Create 30 multiple choice questions on reasoning, programming and communications"
                    }
                ]
            },
            context=Context(requester_id="1", difficulty="intermediate", job_role="software engineer")  
        )
        print(result)

    asyncio.run(main())
