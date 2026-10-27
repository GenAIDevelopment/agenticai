from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from helper import parse_message

MODEL_NAME = 'claude-haiku-4-5'

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an helpful assistant",
        setting_sources=[],
        model=MODEL_NAME,
        max_turns=30,
    )
    question = "What is my name?"
    async for message in query(prompt=question, options=options):
        parse_message(message)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
