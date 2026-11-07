from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import os
from calc_tools import add, sub, mul, div, modulus


def main(session_id="session_101"):
    session = SQLiteSession(
        session_id=session_id,
        db_path="calculator_memory.db"
    )
    MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-5.6-luna')
    agent = Agent(
        name="Smart Calculator",
        model=MODEL_NAME,
        tools= [add, sub, mul, div, modulus],
        instructions=""" 
    You are a helpful calculator assistant

    Understand Mathemetics questions in natural language.

    Always use the provided calculator tools for arthemetic operations

    Use appropritate tools for addition, subtraction, multiplication, division or modulus

    Explain the final answer simply
""" 
    )
    result = Runner.run_sync(
        agent,
        "How many apples do i have now ?",
        session=session
    )
    print(result.final_output)
    result = Runner.run_sync(
            agent,
            "I have purchsed 20 apples more, how  many aapples do i have now ",
            session=session
        )
    print(result.final_output)
    



if __name__ == "__main__":
    load_dotenv()
    
    main()