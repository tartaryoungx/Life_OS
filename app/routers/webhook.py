from fastapi import APIRouter, HTTPException, Request, Header
from app.services.line_handler import handler
from linebot.exceptions import InvalidSignatureError

SCOPES=["https://www.googleapis.com/auth/calendar"]

router = APIRouter(prefix="/api" , tags=["Line_webhook"])

@router.post("/webhook2")
async def webhook(
    request: Request,
    x_line_signature: str = Header(None),
):
    return await handle_line_webhook(
        request=request,
        signature=x_line_signature,
    )

    
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

