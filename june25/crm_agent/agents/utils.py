from dotenv import load_dotenv
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain.chat_models.base import BaseChatModel
import os

load_dotenv()


def get_connection_string() -> str:
    """
    This function gets the connection string 
    """
    connection_string = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    return connection_string


def get_llm() -> BaseChatModel:
    """This method gets the llm
    """
    model_id="gemini-2.5-flash-preview-05-20"
    llm = init_chat_model(model=model_id,  model_provider="google_vertexai")
    return llm

def get_sql_database_toolkit(llm: BaseChatModel) -> SQLDatabaseToolkit:
    """
    This function gets the sql database toolkit 
    """ 
    engine = create_engine(
        get_connection_string(),
        echo=True)
    database = SQLDatabase(engine)
    toolkit = SQLDatabaseToolkit(db=database, llm=llm)
    return toolkit
