from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str
    user_id: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str  # In Supabase, typically a UUID or integer. We'll represent it as str for compatibility.
    created_at: datetime

    class Config:
        from_attributes = True
