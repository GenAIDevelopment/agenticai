from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model


def get_llm(name, provider):
    return init_chat_model(model=name, model_provider=provider)


model_name = "gemini-2.5-flash"
model_provider = "google_vertexai"
gemini_llm = get_llm(model_name, model_provider)

server_params = StdioServerParameters(
    command=r"C:\khajaclassroom\GenerativeAI\agenticai\june25\langgraph-learning\.venv\Scripts\python.exe",
    # Make sure to update to the full absolute path to your math_server.py file
    args=[r"C:\khajaclassroom\GenerativeAI\agenticai\june25\langgraph-learning\experiments\mcp_math.py"],
)


def main():
    async def sync_adapter():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                # Get tools
                tools = await load_mcp_tools(session)
                gemini_llm_with_mcp_tools = gemini_llm.bind_tools(tools)

                # Ask LLM
                response = await gemini_llm_with_mcp_tools.ainvoke(
                    [HumanMessage(
                        content="I have 10 bikes i sold one, How many bikes do i have left ?")]
                )
                print(response)

    asyncio.run(sync_adapter())


# Call your main function synchronously
main()
