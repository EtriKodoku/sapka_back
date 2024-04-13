import secrets
from mail import make_message, send_conf_mail_to
from db import get_db
from ai import get_ai
from models import LoginUser
from fastapi import APIRouter, Depends, Request, WebSocket
from pymongo import MongoClient
from anthropic import Anthropic

router = APIRouter(prefix="/ai")


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
        with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-sonnet-20240229", system="") as stream:
            for text in stream.text_stream:
                msg_buf += text
                await websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})
        await websocket.send_json({"role": "finished", "text": msg_buf})

    return {"ok": True}
