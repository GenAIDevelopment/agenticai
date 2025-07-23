"""This module will have pydantic models
"""

from enum import Enum
from pydantic import BaseModel, Field


class TextPostModel(BaseModel):
    """This class represents the model for linked posts
    """
    token: str = Field(..., description="access token for linked in")
    message: str = Field(..., description="message to be posted")


class ResponseState(Enum):
    """Response State
    """
    SUCCESS = "Success"
    FAILURE = "Failed"
