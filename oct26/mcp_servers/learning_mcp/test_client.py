from mcp import Client, StdioServerParameters
import asyncio
from typing import Any

tools_dict: dict[str,Any] = {}

async def main() -> None:
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.list_tools()

        for tool in result.tools:
            tools_dict[tool.name] = tool.input_schema

        while True:
            print("Tools available")
            for name in tools_dict:
                print(f"name: {name}")
            choice = input("Enter the tool name: ")
            if choice in tools_dict:
                a = int(input('enter the value of a: '))
                b = int(input('enter the value of b: '))
                tool_call_result = await client.call_tool(choice, {'a': a, 'b': b})
                print(tool_call_result)
                print(f"result = {tool_call_result.structured_content['result']}")

            choice = input("Enter q to quit anything else to continue: ")
            if choice.strip().lower() == 'q':
                break







            

if __name__ == "__main__":
    asyncio.run(main())