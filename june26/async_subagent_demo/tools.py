"""This module will contain all the relevant tools to be used by 
agents and subagents
"""

from langchain_tavily import TavilySearch
from dotenv import load_dotenv


def get_web_search() -> TavilySearch:
    """This tool will search the Web"""
    load_dotenv()
    web_search = TavilySearch(
        max_results=10,
        topic="general"
    )
    return web_search
