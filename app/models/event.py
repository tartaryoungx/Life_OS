from pydantic import BaseModel
from typing import Optional, List

class EventBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    location: Optional[str] = None
    reminders: List[str] = []
    calendar_event_id: Optional[str] = None
    user_id: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    reminders: Optional[List[str]] = None
    calendar_event_id: Optional[str] = None

class Event(EventBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True
