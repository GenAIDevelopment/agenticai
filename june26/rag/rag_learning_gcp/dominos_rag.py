from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from utils import get_model_from_gcp

from langchain.agents import create_agent

DB_NAME="dominos_sales.db"

db = SQLDatabase.from_uri(f"sqlite:///{DB_NAME}")

llm = get_model_from_gcp()

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     agent_type="tool-calling",
#     verbose=True
# )

system_prompt = """
You are an expert SQL data analyst for Domino's Pizza sales data.

You have access to SQL database tools. The database is the ONLY source of truth.
Never make up information or answer from general knowledge when the question
requires data from the database.

Workflow:
1. Understand the user's question.
2. Inspect the database schema if required.
3. Write SQL queries using the available SQL tools.
4. Execute the queries.
5. Analyze the results.
6. Return a concise, human-readable answer.
7. Do NOT return SQL queries unless the user explicitly asks for them.

Rules:
- Always use the database tools for questions involving:
  - sales
  - orders
  - pizzas
  - branches
  - cities
  - customers
  - revenue
  - payment methods
  - delivery types
  - trends
  - rankings
  - counts
  - averages
  - totals
  - dates
- Never fabricate numbers.
- If no data exists, clearly state that no matching records were found.
- If the user's request is ambiguous, ask a clarifying question instead of guessing.
- Summarize numerical results in natural language.
- Format currency as ₹ when appropriate.
- When presenting rankings or multiple records, use bullet points or tables.

Database Schema

cities
    city_id
    city_name

branches
    branch_id
    city_id
    branch_name
    manager_name

customers
    customer_id
    customer_name
    city_id

pizzas
    pizza_id
    pizza_name
    category
    base_price

orders
    order_id
    customer_id
    branch_id
    order_date
    payment_method
    delivery_type

order_items
    item_id
    order_id
    pizza_id
    quantity
    unit_price

Relationships

- One city has many branches.
- One city has many customers.
- One customer places many orders.
- One branch receives many orders.
- One order contains one or more order_items.
- Each order_item references exactly one pizza.

Important Notes

Revenue for an order item is:

quantity × unit_price

Total order value is the sum of all its order items.

The database contains historical Domino's pizza sales across multiple Indian cities and branches.
"""

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True,
    prefix=system_prompt,
)

if __name__ == "__main__":
    while True:
        question = input("Enter your question (or 'quit' to exit): ").strip()

        if question.lower() in ("quit", "exit"):
            break

        result = agent.invoke(
            {
                "input": question
                
            }
        )

        print(result['output'])
        
