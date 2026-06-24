from fastapi import APIRouter, HTTPException, Request, Header
from app.services.line_handler import handler
from linebot.exceptions import InvalidSignatureError
import time

SCOPES=["https://www.googleapis.com/auth/calendar"]

router = APIRouter(prefix="/api" , tags=["Line_webhook"])

@router.post("/webhook2")
async def webhook(
    request: Request,
    x_line_signature: str = Header(None),
):
    start = time.perf_counter()
    result = await handle_line_webhook(
        request=request,
        signature=x_line_signature,
    )
    end = time.perf_counter()
    print(f"all time: {end - start:.4f}s")
    return result

    
async def handle_line_webhook(request: Request, signature: str):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        handler.handle(body_str, signature)
    except InvalidSignatureError:
        raise HTTPException(
            status_code=400,
            detail="Invalid signature. Please check Channel Secret."
        )

    return "OK"
#https://console.cloud.google.com/

