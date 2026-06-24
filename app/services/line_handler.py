from app.config import settings
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    QuickReply, QuickReplyButton, MessageAction
)
from app.session.session_redis import StateManager

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
        
    user_id = event.source.user_id
    user_input = event.message.text

    # Call state manager to process message
    result = StateManager.handle_message(user_id, user_input)

    reply_text = result["reply_text"]
    quick_replies = result["quick_replies"]

    # Build Quick Replies if any
    qr_obj = build_reply(quick_replies)

    # Reply message to LINE user
    message_to_send = TextSendMessage(text=reply_text, quick_reply=qr_obj)
    line_bot_api.reply_message(event.reply_token, message_to_send)

def build_reply(quick_replies):
    qr_obj = None
    if quick_replies:
        qr_buttons = []
        for option in quick_replies:
            # Label is capped at 20 characters in LINE
            label = option[:20]
            qr_buttons.append(
                QuickReplyButton(action=MessageAction(label=label, text=option))
            )
        qr_obj = QuickReply(items=qr_buttons)

    return qr_obj 