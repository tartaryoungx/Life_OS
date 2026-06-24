import json
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from linebot import LineBotApi
from linebot.models import TextSendMessage

from app.config import settings

app = FastAPI()

CALENDAR_ID = "tartaryoungx@gmail.com"
TZ = ZoneInfo("Asia/Bangkok")

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def get_calendar_service():
    creds_data = settings.GOOGLE_CALENDAR_CREDENTIALS

    if not creds_data:
        raise RuntimeError("GOOGLE_CALENDAR_CREDENTIALS is missing")

    scopes = ["https://www.googleapis.com/auth/calendar"]

    creds = service_account.Credentials.from_service_account_info(
        creds_data,
        scopes=scopes
    )

    return build("calendar", "v3", credentials=creds)


async def send_line_reminder_later(user_id: str, seconds: int):
    print(f">>> LINE reminder scheduled in {seconds} seconds for user: {user_id}")

    await asyncio.sleep(seconds)

    print(">>> Sending LINE push reminder now")

    line_bot_api.push_message(
        user_id,
        TextSendMessage(text="⏰ Reminder test: อีก 5 นาทีถึง event แล้ว")
    )

    print(">>> LINE push sent")


@app.get("/")
def root():
    return {
        "ok": True,
        "message": "Test reminder server is running"
    }


@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()

        print("=== LINE WEBHOOK BODY ===")
        print(json.dumps(body, indent=2, ensure_ascii=False))

        events = body.get("events", [])
        if not events:
            print(">>> No LINE events")
            return {"ok": True, "message": "No events"}

        line_event = events[0]

        if line_event.get("type") != "message":
            print(">>> Not a message event")
            return {"ok": True, "message": "Not a message event"}

        source = line_event.get("source", {})
        user_id = source.get("userId")

        if not user_id:
            print(">>> No userId found")
            return {"ok": False, "message": "No userId found"}

        print(f">>> user_id = {user_id}")

        service = get_calendar_service()

        now = datetime.now(TZ)

        start_dt = now + timedelta(minutes=10)
        end_dt = start_dt + timedelta(minutes=30)

        event_body = {
            "summary": "[TEST] LINE triggered calendar event",
            "description": "Created from LINE webhook test",
            "start": {
                "dateTime": start_dt.isoformat(),
                "timeZone": "Asia/Bangkok"
            },
            "end": {
                "dateTime": end_dt.isoformat(),
                "timeZone": "Asia/Bangkok"
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "popup",
                        "minutes": 5
                    }
                ]
            },
            "colorId": "9"
        }

        print("=== EVENT BODY ===")
        print(json.dumps(event_body, indent=2, ensure_ascii=False))

        event = service.events().insert(
            calendarId=CALENDAR_ID,
            body=event_body
        ).execute()

        print("=== GOOGLE RETURNED ===")
        print(json.dumps(event, indent=2, ensure_ascii=False))

        asyncio.create_task(
            send_line_reminder_later(
                user_id=user_id,
                seconds=300
            )
        )

        print(">>> Background LINE reminder task created")

        return {
            "ok": True,
            "event_id": event.get("id"),
            "event_start": start_dt.isoformat(),
            "google_popup_reminder": "5 minutes before",
            "line_push_in_seconds": 300
        }

    except Exception as e:
        print("!!! ERROR IN WEBHOOK !!!")
        print(repr(e))

        return {
            "ok": False,
            "error": str(e)
        }