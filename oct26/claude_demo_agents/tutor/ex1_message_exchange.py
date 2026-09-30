from dotenv import load_dotenv
import os
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
from helper import base_options, parse_message


async def initiate_conversation():
    options = base_options()
    question = "What is diffference between function and generator"
    count = 0
    async for message in query(prompt=question, options=options):
        count += 1
        print(f"{count}:  {type(message)}")
        parse_message(message=message)


if __name__ == "__main__":
    # load .env
    load_dotenv()
    asyncio.run(initiate_conversation())