
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession

from longterm_tools import (
    UserContext,
    initialize_memory,
    remember_fact,
    recall_fact,
    list_facts,
)

from calc_tools import add, sub, mul, div, modulus

import os


def main(session_id="session_101"):
    """Run the smart calculator agent."""

    initialize_memory()

    # Load user identity from environment
    user_id = os.getenv("USER_ID")

    if not user_id:
        raise ValueError("USER_ID is not configured in .env")

    # Create user context
    context = UserContext(user_id=user_id)

    # Short-term conversation memory
    session = SQLiteSession(
        session_id=session_id,
        db_path="calculator_memory.db"
    )

    MODEL_NAME = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.6-luna"
    )

    agent = Agent[UserContext](
        name="Smart Calculator",
        model=MODEL_NAME,
        tools=[
            add,
            sub,
            mul,
            div,
            modulus,
            remember_fact,
            recall_fact,
            list_facts,
        ],
        instructions="""
        You are a helpful calculator assistant.

        Understand mathematical questions in natural language.

        Always use the provided calculator tools for
        arithmetic operations.

        Use appropriate tools for addition, subtraction,
        multiplication, division or modulus.

        Explain the final answer simply.

        Memory Rules:
        - When the user explicitly asks to remember a fact,
          call remember_fact before confirming it was saved.
        - When the user asks about a previously saved fact,
          call recall_fact.
        - When the user asks what you remember about them,
          call list_facts.
        - Never invent previously stored facts.
        """,
    )

    result = Runner.run_sync(
        agent,
        "I have 10 apples.",
        session=session,
        context=context,
    )

    print("Assistant:", result.final_output)

    result = Runner.run_sync(
        agent,
        "bought two more how many apples do i have",
        session=session,
        context=context,
    )

    print("Assistant:", result.final_output)

    result = Runner.run_sync(
            agent,
            "Remember the max number of apples i can have are 100",
            session=session,
            context=context,
        )
    
    print("Assistant:", result.final_output)

    result = Runner.run_sync(
                agent,
                "How many apples do i have, and how many can i have at max ?",
                session=session,
                context=context,
            )
        
    print("Assistant:", result.final_output)
    


if __name__ == "__main__":
    load_dotenv()
    main("session_102")
