from dotenv import load_dotenv
import os

from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ResultMessage, TextBlock
import asyncio

async def run_query(question:str = "What is captial of France"):
    options = ClaudeAgentOptions(
        cli_path=r"C:\Users\DELL\.local\bin\claude.exe",
        model="claude-haiku-4-5"
    )
    async for message in  query(prompt=question, options=options) :
        print(f"type: {type(message)}")
        if isinstance(message, ResultMessage):
            print(f"cost {message.total_cost_usd}")
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"response: {block.text}")



async def have_conversation():
    await run_query("My name is khaja")
    await run_query("What is my name?")

async def see_if_tools_work():
    #await run_query("Give me the list of all .py files in current folder")
    await run_query("Go to directai.blog and find the latest post")

if __name__ == "__main__":
    load_dotenv()
    #asyncio.run(run_query())
    #asyncio.run(have_conversation())
    asyncio.run(see_if_tools_work())