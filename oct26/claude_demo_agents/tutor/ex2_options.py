from dotenv import load_dotenv
import os
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
from helper import base_options, parse_message
from typing import Literal

TONE_DICT = {
    'DETAILED': """You are a tutor, Explain the question asked in a 
    direct fashion. Ensure you add some examples to answer the question""",
    'REVISION': """ You are a tutor, The question asked is before an exam, 
    Help in quickly revising to recollect the learnt topic and give simple, 
    crisp and necessary stuff.
    """,
    'BEGINNER': """You are a tutor, The question asked by the student who has
    zero or minimal conceptual knowledge. Dont make assumptions, Answer the question
    in a elaborate fashion right from concepts required to answer the question.
    """
}

async def initiate_conversation(
        tone: Literal["DETAILED", "REVISION", "BEGINNER"], 
        question:str ="What is diffference between function and generator?"
    ):
    chosen_tone = TONE_DICT.get(tone, 'BEGINNER')
    print(f"{tone} => {chosen_tone}")
    custom_options = {
        'system_prompt': TONE_DICT.get(tone, 'BEGINNER')
    }

    options = base_options(**custom_options)
    count = 0
    async for message in query(prompt=question, options=options):
        count += 1
        print(f"{count}:  {type(message)}")
        parse_message(message=message)


async def ask_questions():
    question = input("Enter your question: ")
    tone = input("Enter the tone DETAILED REVISION BEGINNER: ")
    await initiate_conversation(tone, question)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(ask_questions())