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


def handle_event_flow(
    manager, user_id: str, text_clean: str, step: str, partial_data: Dict[str, Any]
):

    if step == manager.STEP_E_NAME:
        return handle_event_name (
            manager = manager,
            user_id = user_id,
            partial_data = partial_data,
            text_clean = text_clean)

    elif step == manager.STEP_E_DATE:
        return handle_event_date (
            manager = manager,
            user_id = user_id,
            partial_data = partial_data,
            text_clean = text_clean)

    elif step == manager.STEP_E_TIME:
        return handle_event_time (
            manager = manager,
            user_id = user_id,
            partial_data = partial_data,
            text_clean = text_clean)
    
    elif step == manager.STEP_E_REMINDER:
        return handle_event_reminder (
            manager = manager,
            user_id = user_id,
            partial_data = partial_data,
            text_clean = text_clean)
    
    manager.clear_session(user_id)
    return {
    "reply_text": "Invalid event step. Resetting to main menu. \nHello! Welcome to LINE Work Manager. Please select an option from the menu:\n\n1. Create Project\n2. Create Task\n3. Create Event",
    "quick_replies": ["Create Project", "Create Task", "Create Event"]
    }
       

def handle_event_name (manager, user_id, partial_data, text_clean):
    partial_data["name"] = text_clean
    manager.update_session(
        user_id,
        manager.FLOW_EVENT,
        manager.STEP_E_DATE,
        partial_data
    )
    return {
        "reply_text": "Event day?",
        "quick_replies": day_quick_replies(),
    }

def handle_event_date(manager, user_id, partial_data, text_clean):
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

    partial_data["event_date"] = parsed_day.isoformat()

    manager.update_session(
        user_id,
        manager.FLOW_EVENT,
        manager.STEP_E_TIME,
        partial_data,
    )

    return {
        "reply_text": "เลือกเวลาเริ่ม Event หรือพิมพ์เองได้เลย\nFormat: HH:MM\nExample: 17:00",
        "quick_replies": time_quick_replies(),
    }

def handle_event_time(manager, user_id, partial_data, text_clean) :
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

    event_date = partial_data["event_date"]
    start_dt = datetime.fromisoformat(
    f"{event_date}T{parsed_time.strftime('%H:%M:%S')}"
    )
    end_dt = start_dt + timedelta(hours=1)

    partial_data["start_time"] = start_dt.isoformat()
    partial_data["end_time"] = end_dt.isoformat()

    manager.update_session(
        user_id,
        manager.FLOW_EVENT,
        manager.STEP_E_REMINDER,
        partial_data,
    )

    return {
        "reply_text": "Set Reminders?",
        "quick_replies": reminder_quick_replies(),
    }

def handle_event_reminder(manager, user_id, partial_data, text_clean):
    reminders = parse_reminders(text_clean)
    partial_data["reminders"] = reminders

    # Create Event & Sync to Google Calendar
    db = get_db()
    try:
        # 1. Google Calendar sync
        calendar_event_id = add_event(
            summary=f"[EVENT] {partial_data['name']}",
            start_time_str=partial_data["start_time"],
            end_time_str=partial_data["end_time"],
            reminders_list=reminders,
            color_id="9",
            calendar_Id="tartaryoungx@gmail.com",
        )

        # 2. Insert to DB
        db.table("events").insert(
            {
                "name": partial_data["name"],
                "start_time": partial_data["start_time"],
                "reminders": reminders,
                "calendar_event_id": calendar_event_id,
                "user_id": user_id,
            }
        ).execute()

        reply = (
            f"Event created successfully!\n\n"
            f"Event: {partial_data['name']}\n"
            f"Time: {partial_data['start_time']}\n"
            f"Reminders: {', '.join(reminders)}\n"
            f"Calendar synced."
        )

        manager.clear_session(user_id)
        return {"reply_text": reply, "quick_replies": ["Create Task", "Create Event", "Create Project"]}
    except Exception as e:
        print(f"Error finishing Event creation: {e}")
        manager.clear_session(user_id)
        return {
            "reply_text": f"Error saving event. Details: {str(e)}",
            "quick_replies": ["Main Menu"],
        }
