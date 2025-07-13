"""This is main module
"""
import asyncio
from app.agents.supervisor import get_supervisor
from app.common.llm import get_llm

graph = None

async def initialize():
    global graph
    llm = await get_llm()
    graph = await get_supervisor(llm=llm)

asyncio.run(initialize())

