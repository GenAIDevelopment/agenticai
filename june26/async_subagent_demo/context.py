"""This module contains context related items
"""

from dataclasses import dataclass

@dataclass
class Context:
    requester_id: str
    difficulty: str
    job_role: str