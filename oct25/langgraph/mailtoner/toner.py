from typing import TypedDict
from dotenv import load_dotenv
import os

class EmailState(TypedDict):
    draft: str
    tone: str
    mail: str

load_dotenv()
model_name = os.getenv('MODEL_NAME')

