from pydantic import BaseModel
from typing import List
from datetime import datetime


class AssignTaskSchema(BaseModel):
    title: str
    description: str
    due_date: datetime
    student_ids: List[str]
