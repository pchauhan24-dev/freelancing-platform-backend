from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    category: str
    budget: float = Field(gt=0)
    description: str = Field(min_length=10)
    required_skills: list[str]
    deadline: datetime
    experience_level: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150
    )
    category: Optional[str] = None
    budget: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = Field(
        default=None,
        min_length=10
    )
    required_skills: Optional[list[str]] = None
    deadline: Optional[datetime] = None
    experience_level: Optional[str] = None