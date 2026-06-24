from typing import Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TIMEZONE = "Asia/Bangkok"

def add_event(
    summary: str,
    start_time_str: str,
    end_time_str: str,
    reminders_list: list[str] | None = None,
    color_id: str | None = None,
    calendar_Id: str | None = "primary"
):
    service = create_service()

    event_body = _build_event_body(
        summary=summary,
        start_time_str=start_time_str,
        end_time_str=end_time_str,
        reminders_list=reminders_list,
        color_id=color_id,
    )

    result = service.events().insert(
        calendarId=calendar_Id,
        body=event_body,
    ).execute()

    print(result)
    return result

def create_service():
    #check cred privillage
    creds = Credentials.from_authorized_user_info(
    json.loads(settings.GOOGLE_TOKEN_JSON),
    SCOPES
    )
    #Calendar API connector
    service = build("calendar", "v3", credentials=creds)
    return service

def add_event_test(service, event_body):
    result = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()
    print(result)
    return



def _build_event_body(
    summary: str,
    start_time_str: str,
    end_time_str: str,
    reminders_list: list[str] | None = None,
    color_id: str | None = None,
) -> dict[str, Any]:

    body: dict[str, Any] = {
        "summary": summary,
        "start": {
            "dateTime": start_time_str,
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end_time_str,
            "timeZone": TIMEZONE,
        },
        "reminders": _build_reminders(reminders_list),
    }

    if color_id:
        body["colorId"] = color_id

    return body

def _build_reminders(
    reminders_list: list[str] | None = None,
) -> dict[str, Any]:
    overrides = []

    for reminder in reminders_list or []:
        minutes = _parse_reminder_to_minutes(reminder)

        if minutes is not None:
            overrides.append(
                {
                    "method": "popup",
                    "minutes": minutes,
                }
            )

    return {
        "useDefault": False,
        "overrides": overrides,
    }

def _parse_reminder_to_minutes(reminder: str) -> int | None:
    mapping = {
        "15 minutes before": 15,
        "1 hour before": 60,
        "1 day before": 1440,
        "3 days before": 4320,
        "No reminder": None,
    }

    return mapping.get(reminder)