from dotenv import load_dotenv
from agents import Agent, Runner


def basic_agent():
    agent = Agent(
        name="Helper",
        instructions="You are helpful assistant",
        model="gpt-5-nano"
    )
    result = Runner.run_sync(agent, "My name is Rahul")
    print(result.final_output)
    result = Runner.run_sync(agent, "What is my name")
    print(result.final_output)


if __name__ == "__main__":
    load_dotenv()
    basic_agent()