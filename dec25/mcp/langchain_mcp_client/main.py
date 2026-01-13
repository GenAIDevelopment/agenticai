import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

async def main():
    # create a  client
    client = MultiServerMCPClient({
        "hello-mcp": {
            "transport": "stdio",
            "command": "python",
            "args": ["C:\\khajaclassroom\\GenerativeAI\\agenticai\\dec25\\mcp\\langchain_mcp_client\\server.py"]
        }
    })
    tools = await client.get_tools()
    # for tool in tools:
    #     print(tool)
    llm = init_chat_model("gemini-2.5-flash-lite", model_provider="google_vertexai")
    agent = create_agent(model=llm, tools=tools)

    result = await agent.ainvoke({
        "messages" : [
            {
                "role": "user",
                "content": "What is 2 + 2?"
            }
        ]
    })
    #print(result)
    for message in result["messages"]:
        print(message.content)
    


if __name__ == "__main__":
    asyncio.run(main())
