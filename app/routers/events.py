from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.database import get_db
from app.models.event import EventCreate, EventUpdate
from app.services.calendar_service import add_event

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", status_code=201)
def create_event(event: EventCreate):
    db = get_db()
    try:
        # 1. Create calendar event
        calendar_event_id = add_event(
            summary=f"[EVENT] {event.name}",
            start_time_str=event.start_time,
            end_time_str=event.end_time,
            location=event.location,
            reminders_list=event.reminders
        )

        # 2. Save event
        res = db.table("events").insert({
            "name": event.name,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "location": event.location,
            "reminders": event.reminders,
            "calendar_event_id": calendar_event_id,
            "user_id": event.user_id
        }).execute()
        
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create event.")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_events(user_id: str):
    db = get_db()
    try:
        res = db.table("events").select("*").eq("user_id", user_id).execute()
        return res.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{event_id}")
def update_event(event_id: str, event: EventUpdate):
    db = get_db()
    try:
        # Get existing event
        existing = db.table("events").select("*").eq("id", event_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Event not found.")
        event_data = existing.data[0]

        update_dict = {}
        if event.name is not None:
            update_dict["name"] = event.name
        if event.start_time is not None:
            update_dict["start_time"] = event.start_time
        if event.end_time is not None:
            update_dict["end_time"] = event.end_time
        if event.location is not None:
            update_dict["location"] = event.location
        if event.reminders is not None:
            update_dict["reminders"] = event.reminders
        if event.calendar_event_id is not None:
            update_dict["calendar_event_id"] = event.calendar_event_id

        # Update in database
        res = db.table("events").update(update_dict).eq("id", event_id).execute()

        # Sync update to Google Calendar
        cal_id = update_dict.get("calendar_event_id") or event_data.get("calendar_event_id")
        if cal_id:
            add_event(
                event_id=cal_id,
                summary=f"[EVENT] {update_dict.get('name')}" if "name" in update_dict else None,
                start_time_str=update_dict.get("start_time"),
                end_time_str=update_dict.get("end_time"),
                location=update_dict.get("location"),
                reminders_list=update_dict.get("reminders")
            )

        return res.data[0] if res.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{event_id}")
def delete_event(event_id: str):
    db = get_db()
    try:
        # Get existing event to find calendar_event_id
        existing = db.table("events").select("calendar_event_id").eq("id", event_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Event not found.")
        cal_id = existing.data[0].get("calendar_event_id")

        # Delete from DB
        db.table("events").delete().eq("id", event_id).execute()

        # Delete from Calendar
        if cal_id:
            add_event(cal_id)

        return {"message": f"Event {event_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
