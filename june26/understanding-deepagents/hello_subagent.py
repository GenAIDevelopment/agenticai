from utils import get_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from books_search_tools import get_book_name, get_information_from_book
from internet_search_tools import web_search

model = get_model()
backend = FilesystemBackend(
    root_dir="./agent_workspace",
    virtual_mode=True
)

book_subagent= {
    "name": "book-search-agent",
    "description": "Used to research about any topic in books",
    "system_prompt": "You are a great scholar with access to tools to get any information from any books. First search the book and then for topic in a book",
    "tools": [get_book_name, get_information_from_book],
    "model": model,  # Optional override, defaults to main agent model
}

websearch_subagent = {
    "name": "web-search-agent",
    "description": "Used to research about any topic in web",
    "system_prompt": "You are a great researcher with access to tools to get any information from web.",
    "tools": [web_search],
    "model": model,  # Optional override, defaults to main agent model
}

agent = create_deep_agent(
    model=model,
    backend=backend,
    subagents=[websearch_subagent, book_subagent],
    system_prompt="""You are a researcher. You have access to subagents for book search and web search
    
    Given any topic search both in books and web using sub agents
    Combine the response from both the agents and give a concise version
    Plan for todo items in /subagent_todos.md

    Ensure you write a response from every subagent into /<subagent-name>_response.middleware=

    The final version should not exceed 50 words
    
"""
)

if __name__ == "__main__":
    result = agent.invoke(input= {
        "messages": [{
            "role": "user",
            "content": "I want you to research on Indus Valley Civilization"
        }]
    })