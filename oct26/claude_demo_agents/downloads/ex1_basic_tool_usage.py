from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from helper import parse_message, MODEL_NAME
from pathlib import Path

DOWNLOADS_DIR = Path("downloads/downloads")

async def main():
    options = ClaudeAgentOptions(
            system_prompt="You are an helpful assistant",
            setting_sources=[],
            model=MODEL_NAME,
            max_turns=30,
            tools=["Read", "Glob", "PowerShell"],
            permission_mode="bypassPermissions",
            cwd=DOWNLOADS_DIR,
        )
    async with ClaudeSDKClient(options=options) as client:
        question = input("Give any instruction about downloads folder")
        await client.query(question)
        async for message in client.receive_messages():
            parse_message(message)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())