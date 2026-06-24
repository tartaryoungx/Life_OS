from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.database import get_db
from app.models.task import TaskCreate, TaskUpdate
from app.services.calendar_service import add_event

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", status_code=201)
def create_task(task: TaskCreate):
    db = get_db()
    try:
        # Get project name for calendar description
        proj_res = db.table("projects").select("name").eq("id", task.project_id).execute()
        proj_name = proj_res.data[0]["name"] if proj_res.data else "Unknown"

        # 1. Create calendar event
        calendar_event_id = add_event(
            summary=f"[TASK] {task.name}",
            start_time_str=task.deadline,
            description=f"Task linked to Project: {proj_name}",
            reminders_list=task.reminders
        )

        # 2. Save task
        res = db.table("tasks").insert({
            "name": task.name,
            "project_id": task.project_id,
            "deadline": task.deadline,
            "reminders": task.reminders,
            "calendar_event_id": calendar_event_id,
            "user_id": task.user_id
        }).execute()
        
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create task.")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def list_tasks(user_id: str):
    db = get_db()
    try:
        res = db.table("tasks").select("*").eq("user_id", user_id).execute()
        return res.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}")
def update_task(task_id: str, task: TaskUpdate):
    db = get_db()
    try:
        # Get existing task
        existing = db.table("tasks").select("*").eq("id", task_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Task not found.")
        task_data = existing.data[0]

        update_dict = {}
        if task.name is not None:
            update_dict["name"] = task.name
        if task.project_id is not None:
            update_dict["project_id"] = task.project_id
        if task.deadline is not None:
            update_dict["deadline"] = task.deadline
        if task.reminders is not None:
            update_dict["reminders"] = task.reminders
        if task.calendar_event_id is not None:
            update_dict["calendar_event_id"] = task.calendar_event_id

        # Update in database
        res = db.table("tasks").update(update_dict).eq("id", task_id).execute()

        # Sync update to Google Calendar
        cal_id = update_dict.get("calendar_event_id") or task_data.get("calendar_event_id")
        if cal_id:
            proj_name = "Unknown"
            new_proj_id = update_dict.get("project_id") or task_data.get("project_id")
            if new_proj_id:
                proj_res = db.table("projects").select("name").eq("id", new_proj_id).execute()
                proj_name = proj_res.data[0]["name"] if proj_res.data else "Unknown"

            add_event(
                event_id=cal_id,
                summary=f"[TASK] {update_dict.get('name')}" if "name" in update_dict else None,
                start_time_str=update_dict.get("deadline"),
                description=f"Task linked to Project: {proj_name}" if "project_id" in update_dict else None,
                reminders_list=update_dict.get("reminders")
            )

        return res.data[0] if res.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
def delete_task(task_id: str):
    db = get_db()
    try:
        # Get existing task to find calendar_event_id
        existing = db.table("tasks").select("calendar_event_id").eq("id", task_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Task not found.")
        cal_id = existing.data[0].get("calendar_event_id")

        # Delete from DB
        db.table("tasks").delete().eq("id", task_id).execute()

        # Delete from Calendar
        if cal_id:
            add_event(cal_id)

        return {"message": f"Task {task_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
