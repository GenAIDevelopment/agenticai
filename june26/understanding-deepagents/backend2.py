from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend
from utils import get_model
from deepagents import create_deep_agent


def get_article_points(topic: str) -> str:
    """Simple tool that gives article talking points

    Args:
        topic (str): topic

    Returns:
        str: Talking points
    """
    return f"""
Article Topic: {topic}

Talking Points:
1. Start with the learners confusion
2. Explain the problem in simple language
3. Give a practical example
4. Explain common mistakes
5. End with a short summary
"""


model = get_model()

backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/workspace/": FilesystemBackend(
            root_dir="./agent_workspace",
            virtual_mode=True
        ),
    },
)
agent = create_deep_agent(
    model=model,
    tools=[get_article_points],
    backend=backend,
    system_prompt="""
You are a technical article writing agent.

Workflow:
1. create a short plan with todos and write all the todos to /workspace/todos.md
2. Use the tool to get article points
3. write rough notes /workspace/roughnotes.md
4. Write the final article to /workspace/article.md
5. Return a short summary and mention the files created.

Keep the article begineer friendly
"""
)

if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Write an article on algebra."
                }
            ]
        }
    )
    result["messages"][-1].pretty_print()
