import secrets
from mail import make_message, send_conf_mail_to
from db import get_db
from ai import get_ai
from models import LoginUser
from fastapi import APIRouter, Depends, Request, WebSocket
from pymongo import MongoClient
from anthropic import Anthropic

router = APIRouter(prefix="/ai")
SYSTEM_PROMPT = "You are a psychological AI assistant named Віра. After greeting introduce yourself to user. You need to ask user about different parts of his psychological condition. Don't repeat questions. Just ask next question after you get user answer, don't provide any suggestions. Your time is limited so you need cover as much as you can for least questions. You will speak with user in Ukrainian. User can ask you for a report about his psychological state. Your report is for psychologist, you have to provide only user condition without any suggestions about healing"

@router.websocket('/wschat')
async def wscaht(websocket: WebSocket, ai: Anthropic = Depends(get_ai)):
    await websocket.accept()
    chat_log = []
    while True:
        recieved = await websocket.receive_json()
        if not recieved["role"] == "user":
            await websocket.close()
            return
        chat_log.append({"role": "user", "content": recieved["text"]})
        msg_buf = ""
        print(chat_log)
        with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=SYSTEM_PROMPT) as stream:
            for text in stream.text_stream:
                msg_buf += text
                await websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})
        await websocket.send_json({"role": "finished", "text": msg_buf})

    return {"ok": True}
