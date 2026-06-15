from utils import get_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

model = get_model()
backend = FilesystemBackend(
    root_dir="./new_agent_workspace",
    virtual_mode=True
)

agent = create_deep_agent(
    model=model,
    backend=backend,
    skills=["./skills"],
    system_prompt="""
You are a notes writer with access to skills
Depending on the grade provided or targeted audience specified i.e. high school or primary school student pick the right skill
Create a todo list before writing any notes and store in /todos/<topic>.md
Ensure you validate the notes created and replan todos if required.

Ensure the final notes is created in a folder with /topic-name/<school>/finalnotes.md
create other files if necessary in the folder /topic-name/<school>/
"""
)

if __name__ == "__main__":
    agent.invoke(
        input={
            "messages": [{
                "role": "user",
                "content": "Create a notes for a primary school student on Solar System"
            }]
        }
    )