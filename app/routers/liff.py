# app/routers/liff.py

from datetime import date, datetime, timedelta, timezone
from typing import Optional, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.database import get_db, PostgresClient


router = APIRouter(prefix="/api/liff", tags=["LIFF Dashboard"])


class ToggleTaskRequest(BaseModel):
    is_done: bool


class RescheduleTaskRequest(BaseModel):
    deadline: str


class RescheduleEventRequest(BaseModel):
    start_time: str
    end_time: Optional[str] = None


class DeleteItemRequest(BaseModel):
    item_type: Literal["event", "task"]
    item_id: UUID


def get_text_date(value: str) -> Optional[str]:
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except Exception:
        try:
            return date.fromisoformat(value).isoformat()
        except Exception:
            return None


@router.get("/today")
def get_today_items(
    user_id: str = Query(...),
    db: PostgresClient = Depends(get_db),
):
    today = date.today().isoformat()

    events = db.table("events").select("*").eq("user_id", user_id).execute().data
    tasks = db.table("tasks").select("*").eq("user_id", user_id).execute().data

    today_events = [
        event for event in events
        if event.get("start_time", "").startswith(today)
    ]

    today_tasks = [
        task for task in tasks
        if task.get("deadline", "").startswith(today)
    ]

    return {
        "date": today,
        "events": today_events,
        "tasks": today_tasks,
    }


@router.get("/days")
def get_items_by_days(
    user_id: str = Query(...),
    start_date: date = Query(default_factory=date.today),
    days: int = Query(default=7, ge=1, le=31),
    db: PostgresClient = Depends(get_db),
):
    events = db.table("events").select("*").eq("user_id", user_id).execute().data
    tasks = db.table("tasks").select("*").eq("user_id", user_id).execute().data

    stack = {}

    for i in range(days):
        d = start_date + timedelta(days=i)
        stack[d.isoformat()] = {
            "date": d.isoformat(),
            "events": [],
            "tasks": [],
        }

    for event in events:
        event_date = get_text_date(event.get("start_time", ""))
        if event_date in stack:
            stack[event_date]["events"].append(event)

    for task in tasks:
        task_date = get_text_date(task.get("deadline", ""))
        if task_date in stack:
            stack[task_date]["tasks"].append(task)

    return {
        "start_date": start_date.isoformat(),
        "days": list(stack.values()),
    }


@router.patch("/tasks/{task_id}/toggle")
def toggle_task(
    task_id: UUID,
    payload: ToggleTaskRequest,
    user_id: str = Query(...),
    db: PostgresClient = Depends(get_db),
):
    completed_at = datetime.now(timezone.utc).isoformat() if payload.is_done else None

    result = (
        db.table("tasks")
        .update({
            "is_done": payload.is_done,
            "completed_at": completed_at,
        })
        .eq("id", str(task_id))
        .eq("user_id", user_id)
        .execute()
        .data
    )

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result[0]


@router.patch("/tasks/{task_id}/reschedule")
def reschedule_task(
    task_id: UUID,
    payload: RescheduleTaskRequest,
    user_id: str = Query(...),
    db: PostgresClient = Depends(get_db),
):
    result = (
        db.table("tasks")
        .update({"deadline": payload.deadline})
        .eq("id", str(task_id))
        .eq("user_id", user_id)
        .execute()
        .data
    )

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result[0]


@router.patch("/events/{event_id}/reschedule")
def reschedule_event(
    event_id: UUID,
    payload: RescheduleEventRequest,
    user_id: str = Query(...),
    db: PostgresClient = Depends(get_db),
):
    result = (
        db.table("events")
        .update({
            "start_time": payload.start_time,
            "end_time": payload.end_time,
        })
        .eq("id", str(event_id))
        .eq("user_id", user_id)
        .execute()
        .data
    )

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")

    return result[0]


@router.delete("/items")
def delete_item(
    payload: DeleteItemRequest,
    user_id: str = Query(...),
    db: PostgresClient = Depends(get_db),
):
    table_name = "events" if payload.item_type == "event" else "tasks"

    result = (
        db.table(table_name)
        .delete()
        .eq("id", str(payload.item_id))
        .eq("user_id", user_id)
        .execute()
        .data
    )

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "ok": True,
        "deleted_type": payload.item_type,
        "deleted_id": str(payload.item_id),
    }