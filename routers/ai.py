import secrets
from mail import make_message, send_conf_mail_to
from db import get_db
from ai import get_ai, get_stream_with_log
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
        rtext = await websocket.receive_text()
        print(rtext)
        recieved = await websocket.receive_json()
        print("IRECIEVED", recieved)
        if not recieved["role"] == "user":
            await websocket.close()
            return
        chat_log.append({"role": "user", "content": recieved["text"]})
        msg_buf = ""
        break
        chat_stream = await get_stream_with_log(ai, chat_log)
        for text in chat_stream:
            msg_buf += text
            websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})
        websocket.send_json({"role": "finished", "text": msg_buf})

    return {"ok": True}
