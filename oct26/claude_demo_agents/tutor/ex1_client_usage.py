from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, InMemorySessionStore, query
import asyncio
from helper import parse_message

MODEL_NAME = 'claude-haiku-4-5'

async def main():
    #session_storage = InMemorySessionStore()
    options = ClaudeAgentOptions(
        system_prompt="You are an helpful assistant",
        setting_sources=[],
        model=MODEL_NAME,
        max_turns=30,
        #session_id="4279dd53-b7a2-46b9-8ac0-065d7130330c",
        resume="4279dd53-b7a2-46b9-8ac0-065d7130330c",
        #session_store=session_storage
    )
    # async with ClaudeSDKClient(options=options) as client:
    #     # question = "My name is khaja and i live in hyderabad"
    #     # await client.query(question)
    #     # async for message in client.receive_messages():
    #     #     parse_message(message)

    #     question = "Where do i live?"

    #     await client.query(question)
    #     async for message in client.receive_messages():
    #         parse_message(message)
    question = "What is my name?"
    async for message in query(prompt=question, options=options):
        parse_message(message)








if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
