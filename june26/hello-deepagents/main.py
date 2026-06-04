from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        project=os.getenv('PROJECT_ID')
    )
    result = model.invoke("What is 5 plus 3?")
    print(result.content)
    
    agent = create_deep_agent(
        #model="google_genai:gemini-3.5-flash",
        model=model,
        tools=[],
        system_prompt="You are a helpful assistant."
    )
    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "What is 5 plus 3?"
            }
        ]
    })
    for message in result['messages']:
        message.pretty_print()


if __name__ == "__main__":
    main()
