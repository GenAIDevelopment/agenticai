"""
This module will contain response format
"""
from pydantic import BaseModel, Field
from typing import Literal


class MultipleChoiceQuestion(BaseModel):
    """Multiple Choice Question"""
    question: str = Field(description="Question")
    A: str = Field(description="Choice A")
    B: str = Field(description="Choice B")
    C: str = Field(description="Choice C")
    D: str = Field(description="Choice D")

    answer: Literal["A", "B", "C", "D"] = Field(
        description="Correct answer"
    )

    explanation: str = Field(description="Explanation to answer")

class SubAgentResponse(BaseModel):
    """SubAgent Response Format"""
    mcqs: list[MultipleChoiceQuestion] = Field(
        min_length=1,
        description="List of MCQs"
    )
    topic: str = Field(
        min_length=1,
        description="Topic name"
    )
