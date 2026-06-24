from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    name: str
    project_id: str
    deadline: str  # We store as ISO 8601 string or parsed date string
    reminders: List[str] = []
    calendar_event_id: Optional[str] = None
    user_id: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[str] = None
    deadline: Optional[str] = None
    reminders: Optional[List[str]] = None
    calendar_event_id: Optional[str] = None

class Task(TaskBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True
