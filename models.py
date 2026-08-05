from typing import List
from pydantic import BaseModel, Field

class Issue(BaseModel):
    id: str
    title: str
    url: str
    description: str = ""
    repository: str = ""
    labels: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    score: int = 0
    created_at: str = ""
    comments_count: int = 0
