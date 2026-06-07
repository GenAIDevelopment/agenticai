import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """Create and return a SQLAlchemy engine configured with the database URL
    from environment variables.

    Returns:
        Engine: A SQLAlchemy Engine instance for connecting to the database.
    """
    load_dotenv()

    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://ccuser:ccpassword@localhost:5432/customer_care",
    )
    engine = create_engine(db_url)
    return engine

def execute_one(query:str, params:dict | None = None):
    with get_engine().begin() as conn:
        result = conn.execute(text(query), params)
        return result.fetchone()
    
def execute_many(query:str, params:dict | None = None):
    with get_engine().begin() as conn:
        result = conn.execute(text(query), params)
        return result.fetchall()
    
def execute_write(query:str, params:dict | None = None):
    with get_engine().begin() as conn:
        result = conn.execute(text(query), params)
        conn.commit()
        return result.fetchone()



if __name__ == "__main__":
    engine = get_engine()

    # Test the connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(result.fetchone())
    except Exception as e:
        print(f"Failed to connect to database: {e}")
