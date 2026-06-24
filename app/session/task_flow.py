from typing import Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.services.calendar_service import add_event
from app.utils.datetime_helper import (
    day_quick_replies,
    time_quick_replies,
    reminder_quick_replies,
    parse_day,
    parse_time,
    parse_reminders,
)


def handle_task_flow(
    manager,
    user_id: str,
    text_clean: str,
    step: str,
    partial_data: Dict[str, Any],
):
    if step == manager.STEP_T_NAME:
        return handle_task_name(
            manager=manager,
            user_id=user_id,
            partial_data=partial_data,
            text_clean=text_clean,
        )

    elif step == manager.STEP_T_PROJECT:
        return handle_task_project(
            manager=manager,
            user_id=user_id,
            partial_data=partial_data,
            text_clean=text_clean,
        )

    elif step == manager.STEP_T_DEADLINE_DAY:
        return handle_task_deadline_day(
            manager=manager,
            user_id=user_id,
            partial_data=partial_data,
            text_clean=text_clean,
        )

    elif step == manager.STEP_T_DEADLINE_TIME:
        return handle_task_deadline_time(
            manager=manager,
            user_id=user_id,
            partial_data=partial_data,
            text_clean=text_clean,
        )

    elif step == manager.STEP_T_REMINDER:
        return handle_task_reminder(
            manager=manager,
            user_id=user_id,
            partial_data=partial_data,
            text_clean=text_clean,
        )

    manager.clear_session(user_id)

    return {
        "reply_text": (
            "Invalid task step. Resetting to main menu.\n"
            "Hello! Welcome to LINE Work Manager. Please select an option from the menu:\n\n"
            "1. Create Project\n"
            "2. Create Task\n"
            "3. Create Event"
        ),
        "quick_replies": ["Create Project", "Create Task", "Create Event"],
    }

def _fetch_user_projects(user_id):
    try:
        db = get_db()
        res = db.table("projects").select("id, name").eq("user_id", user_id).execute()
        return res.data or []
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []


def _build_project_options(projects):
    options_str = "\n".join([f"{i + 1}. {p['name']}" for i, p in enumerate(projects)])
    quick_replies = [str(i + 1) for i in range(len(projects))]
    quick_replies.append("Cancel")
    return options_str, quick_replies

def handle_task_name(manager, user_id, partial_data, text_clean):
    partial_data["name"] = text_clean

    projects = _fetch_user_projects(user_id)

    if not projects:
        manager.clear_session(user_id)
        return {
            "reply_text": "You don't have any Projects yet. Please create a Project first before creating a Task.",
            "quick_replies": ["Create Project", "Main Menu", "Cancel"],
        }

    partial_data["project_options"] = projects

    manager.update_session(
        user_id,
        manager.FLOW_TASK,
        manager.STEP_T_PROJECT,
        partial_data,
    )

    options_str, quick_replies = _build_project_options(projects)

    return {
        "reply_text": f"Link to which Project?\n\n{options_str}",
        "quick_replies": quick_replies,
    }


def handle_task_project(manager, user_id, partial_data, text_clean):
    projects = partial_data.get("project_options", [])

    selected_project_id = None
    selected_project_name = None

    try:
        idx = int(text_clean) - 1

        if 0 <= idx < len(projects):
            selected_project_id = projects[idx]["id"]
            selected_project_name = projects[idx]["name"]

    except ValueError:
        for project in projects:
            if project["name"].lower() == text_clean.lower():
                selected_project_id = project["id"]
                selected_project_name = project["name"]
                break

    if not selected_project_id:
        options_str, quick_replies = _build_project_options(projects)

        return {
            "reply_text": f"Invalid project selection. Please choose a number or name:\n\n{options_str}",
            "quick_replies": quick_replies,
        }

    partial_data["project_id"] = selected_project_id
    partial_data["project_name"] = selected_project_name
    partial_data.pop("project_options", None)

    manager.update_session(
        user_id,
        manager.FLOW_TASK,
        manager.STEP_T_DEADLINE_DAY,
        partial_data,
    )

    return {
        "reply_text": "Deadline day?",
        "quick_replies": day_quick_replies(),
    }


def handle_task_deadline_day(manager, user_id, partial_data, text_clean):
    if text_clean.strip().lower() == "custom date":
        return {
            "reply_text": "Please type date in format: DD/MM/YYYY\nExample: 05/06/2026",
            "quick_replies": ["Cancel"],
        }

    parsed_day = parse_day(text_clean)

    if not parsed_day:
        return {
            "reply_text": "Invalid date format. Please type date in format: DD/MM/YYYY\nExample: 05/06/2026",
            "quick_replies": day_quick_replies() + ["Cancel"],
        }

    partial_data["deadline_day"] = parsed_day.isoformat()

    manager.update_session(
        user_id,
        manager.FLOW_TASK,
        manager.STEP_T_DEADLINE_TIME,
        partial_data,
    )

    return {
        "reply_text": "เลือกเวลา Deadline หรือพิมพ์เองได้เลย\nFormat: HH:MM\nExample: 17:00",
        "quick_replies": time_quick_replies(),
    }


def handle_task_deadline_time(manager, user_id, partial_data, text_clean):
    if text_clean.strip().lower() == "custom time":
        return {
            "reply_text": "Please type time in format: HH:MM\nExample: 17:00",
            "quick_replies": ["Cancel"],
        }

    parsed_time = parse_time(text_clean)

    if not parsed_time:
        return {
            "reply_text": "Invalid time format. Please type time in format: HH:MM\nExample: 17:00",
            "quick_replies": time_quick_replies(),
        }

    deadline_day = partial_data["deadline_day"]

    deadline_dt = datetime.fromisoformat(
        f"{deadline_day}T{parsed_time.strftime('%H:%M:%S')}"
    )

    deadline_end_dt = deadline_dt + timedelta(hours=1)

    partial_data["deadline"] = deadline_dt.isoformat()
    partial_data["deadline_end"] = deadline_end_dt.isoformat()

    manager.update_session(
        user_id,
        manager.FLOW_TASK,
        manager.STEP_T_REMINDER,
        partial_data,
    )

    return {
        "reply_text": "Set Reminders?",
        "quick_replies": reminder_quick_replies(),
    }


def handle_task_reminder(manager, user_id, partial_data, text_clean):
    reminders = parse_reminders(text_clean)
    partial_data["reminders"] = reminders

    db = get_db()

    try:
        calendar_event_id = add_event(
            summary=f"[TASK] {partial_data['name']}",
            start_time_str=partial_data["deadline"],
            end_time_str=partial_data["deadline_end"],
            reminders_list=reminders,
            color_id="2",
            calendar_Id="3e9506504fc9c6ff5f8cf039e8678378c55113cc90c5f261ebff19a5f0b3f2ea@group.calendar.google.com",
        )

        db.table("tasks").insert(
            {
                "name": partial_data["name"],
                "project_id": partial_data["project_id"],
                "deadline": partial_data["deadline"],
                "reminders": reminders or [],
                "calendar_event_id": calendar_event_id,
                "user_id": user_id,
            }
        ).execute()

        reply = (
            f"Task created successfully!\n\n"
            f"Task: {partial_data['name']}\n"
            f"Project: {partial_data['project_name']}\n"
            f"Deadline: {partial_data['deadline']}\n"
            f"Reminders: {', '.join(reminders) if reminders else 'No reminder'}\n"
            f"Calendar synced."
        )

        manager.clear_session(user_id)

        return {
            "reply_text": reply,
            "quick_replies": ["Create Task", "Create Event", "Create Project"],
        }

    except Exception as e:
        print(f"Error finishing Task creation: {e}")
        manager.clear_session(user_id)

        return {
            "reply_text": f"Error saving task. Details: {str(e)}",
            "quick_replies": ["Main Menu"],
        }