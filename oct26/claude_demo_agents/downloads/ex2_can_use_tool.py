from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from helper import parse_message, MODEL_NAME
from pathlib import Path



from claude_agent_sdk.types import (
    PermissionResultAllow, 
    PermissionResultDeny, 
    ToolPermissionContext
)

DOWNLOADS_DIR = Path("downloads/downloads")

# 1. Define the callback function
async def custom_tool_checker(
    tool_name: str, 
    input_data: dict, 
    context: ToolPermissionContext
) -> PermissionResultAllow | PermissionResultDeny:
    
    print(f"\nTool Requested: {tool_name}")
    print(f"Inputs: {input_data}")
    
    # Simple console approval check
    user_response = input("Allow Claude to run this tool? (y/n): ")
    
    if user_response.lower() == 'y':
        return PermissionResultAllow(behavior='allow')
    else:
        return PermissionResultDeny(behavior='deny', reason="User rejected the tool execution.")



async def main():
    options = ClaudeAgentOptions(
            system_prompt="You are an helpful assistant",
            setting_sources=[],
            model=MODEL_NAME,
            max_turns=30,
            tools=["Read", "Glob", "PowerShell"],
            cwd=DOWNLOADS_DIR,
            permission_mode="default",
            can_use_tool=custom_tool_checker
        )
    async with ClaudeSDKClient(options=options) as client:
        question = input("Give any instruction about downloads folder")
        await client.query(question)
        async for message in client.receive_messages():
            parse_message(message)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())