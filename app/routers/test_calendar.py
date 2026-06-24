from fastapi import APIRouter, HTTPException, Request, Header
from app.services.calendar_service import create_service, add_event_test
from app.services.line_handler import handler
from linebot.exceptions import InvalidSignatureError
from app.session.state_manager_db import StateManager
from app.database import get_db
from app.redis_client import redis_client

SCOPES=["https://www.googleapis.com/auth/calendar"]

router = APIRouter(prefix="/test" , tags=["Test"])

@router.post("/calendar")
async def webhook():
    #handle_line_webhook(request=request, signature=x_line_signature)
    service = create_service()
    event_body = {
        "summary": "ss",   
        "start": {
            "dateTime": "2026-06-29T17:00:00",
            "timeZone": "Asia/Bangkok"
        },

        "end": {
            "dateTime": "2026-06-29T18:00:00",
            "timeZone": "Asia/Bangkok"
        },
     
        "colorId": "4"
    }
    try:
        add_event_test(
            service=service,
            event_body=event_body,
        )
        return {"ok": True,}

    except Exception as e:
        print("CALENDAR ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    

async def handle_line_webhook(request: Request, signature: str):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        await handler.handle(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400,
            detail="Invalid signature. Please check Channel Secret."
        )

    return "OK"
#https://console.cloud.google.com/
    

"""
{
        "summary": event_name,        

        "start": {
            "dateTime": "2026-06-23T17:00:00",
            "timeZone": "Asia/Bangkok"
        },

        "end": {
            "dateTime": "2026-06-23T18:00:00",
            "timeZone": "Asia/Bangkok"
        },

        "reminders": {
            "useDefault": False,
            "overrides": [
                {
                    "method": "popup",
                    "minutes": 10
                },
                {
                    "method": "popup",
                    "minutes": 60
                }
            ]
        },

        "colorId": "4"
    }
"""

@router.post("/db")
async def test_db():
    db = get_db()
    results = db.table("events").select("*").eq("name","Test").execute()
    result = {
        "data": results.data ,
        "execution_time": results.execution_time,
        "sql": results.sql,
        }
    #rows = db_connecter()

    return result

@router.post("/redis")
async def test_redis():
    a=redis_client.set("test", "hello")
    print(redis_client.get("test"))
    return a