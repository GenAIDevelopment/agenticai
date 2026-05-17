from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


load_dotenv()
project = os.getenv('GOOGLE_CLOUD_PROJECT')



# def main():
#     result = llm.invoke("What is captial of france")
#     result.pretty_print()
async def main():
    # model
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash-lite",
        vertexai = True,
        project = project
    )
    client = MultiServerMCPClient({
        "library-mcp": {
            "transport": "http",
            "url": "http://localhost:19000/mcp"
        }
    })
    tools = await client.get_tools()
    agent = create_agent(llm, tools)

    result = await agent.ainvoke({
        "messages": "Add the following book to library using library mcp  {'book_id':'B011','title':'The Power of Habit','author':'Charles Duhigg','published_year':2012,'available_copies':6,'total_copies':10,'genre':'Self Help','available':True,'active':True,'tags':['habits','productivity','self-improvement'],'isbn':'9780812981605'}" 
    })

    print(result)


    

if __name__ == "__main__":
    asyncio.run(main())
