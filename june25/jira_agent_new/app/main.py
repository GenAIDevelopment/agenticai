"""This is main module
"""
from agents.supervisor import get_supervisor
from common.llm import get_llm

llm = get_llm()
graph = get_supervisor(llm=llm)

