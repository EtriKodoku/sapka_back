from db import get_db
from ai import get_ai
from models import Report
from fastapi import APIRouter, Depends, WebSocket
from pymongo import MongoClient
from anthropic import Anthropic

router = APIRouter(prefix="/ai")
SYSTEM_PROMPT = "You are a psychological AI assistant named Віра that analyzes user condition and provide the best review for professional psychological support. After greeting introduce yourself to user. You need to ask user about different parts of his psychological condition. Don't repeat questions. Just ask next question after you get user answer, don't provide any suggestions. Your question shouldn't be dry. Your time is limited so you need cover as much as you can for least questions. You will speak with user in Ukrainian. User can ask you for a report about his psychological state. Your report is for psychologist, you have to provide only user condition without any suggestions about healing"

@router.websocket('/wschat')
async def wscaht(websocket: WebSocket, ai: Anthropic = Depends(get_ai), db = Depends(get_db)):
    await websocket.accept()
    chat_log = []
    i = 0       # Index of answer
    limit = 5   # Maximum number of answers
    while True:
        i += 1
        recieved = await websocket.receive_json()
        if not recieved["role"] == "user":
            await websocket.close()
            return
        content = recieved['text']
        if i == limit - 1:
            content = content + ". Постав ще одне останнє питання. Після відповіді користувача на це питання, нових питань не став, подякуй мені за відповіді та повідом, що ти сформуєш звіт та відправиш його на опрацювання професійним психологам."
        

        chat_log.append({"role": "user", "content": content})
        msg_buf = ""
        with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=SYSTEM_PROMPT) as stream:
            for text in stream.text_stream:
                msg_buf += text
                await websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})
        
        await websocket.send_json({"role": "finished", "text": msg_buf})
        if i == limit:
            await websocket.send_json({"role": "lock", "text": ""})
            report = ""
            content = content + ". Жодних запитань більше не став. Тепер ти припиняєш розмову з користувачем. Сформуй звіт для спеціалістів. Надай в повідомленні інформацію лише про стан чи проблему користувача"
            chat_log.append({"role": "user", "content": content})
            
            with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=SYSTEM_PROMPT) as stream:
                for text in stream.text_stream:
                    report += text
                rep_id = str(db["codecon"].reports.insert_one({'text': report, 'rep_type':'Psych'}).inserted_id)
                await websocket.send_json({"role": "end", "text": rep_id})
            break


GLOB_SYSTEM_POMPT = """You are AI-consultant named Віра, created to help peple discover all services that Віра website provides. Your website provides services to people suffering from Ukrainian war.
Here is the list of services:
- Психологічна підтримка :psych:
- Юридична допомога :uri:
- Знайти житло :house:
- Знайти роботу :work:
You can send user a bare message, or append a button to your message that will redirct user to the service. To add button you sould add :service-name: to your message. Your chat with user ends when you recommend a service, so do not use it opportunity too early You can include only one service at a time. When you show user a redirect button please explain your message why you think user neds it. User will write to you in ukrainian language< you should also respond only in ukraian.
"""

@router.websocket('/wsglob')
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
        with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=GLOB_SYSTEM_POMPT) as stream:
            for text in stream.text_stream:
                msg_buf += text
                await websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})
        await websocket.send_json({"role": "finished", "text": msg_buf})
        

   
    return {"ok": True}


LAW_SYSTEM_PROMPT = "You are a legal AI assistant named Віра that analyzes user problem and provide the best review for professional legal support. After greeting introduce yourself to user. You need to ask user about his problem. Just ask next question after you get user answer, don't provide any suggestions. Your question shouldn't be dry. Your time is limited so you need to get as much details as you can for least questions. You will speak with user in Ukrainian. User can ask you for a report about his problem. Your report is for lawyer, you have to describe user problem without any suggesting a solution"

@router.websocket('/wslaw')
async def wscaht(websocket: WebSocket, ai: Anthropic = Depends(get_ai), db = Depends(get_db)):
    await websocket.accept()
    chat_log = []
    i = 0       # Index of answer
    limit = 3   # Maximum number of answers
    while True:
        i += 1
        recieved = await websocket.receive_json()
        if not recieved["role"] == "user":
            await websocket.close()
            return
        content = recieved['text']
        if i == limit - 1:
            content = content + ". Постав ще одне останнє питання. Після відповіді користувача на це питання, нових питань не став, подякуй мені за відповіді та повідом, що ти сформуєш звіт та відправиш його на опрацювання професійним юристам."
        

        chat_log.append({"role": "user", "content": content})
        msg_buf = ""
        with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=SYSTEM_PROMPT) as stream:
            for text in stream.text_stream:
                msg_buf += text
                await websocket.send_json({"role": "part", "text": text})
        chat_log.append({"role": "assistant", "content": msg_buf})

        if i == limit:
            report = ""
            content = content + ". Жодних запитань більше не став. Тепер ти припиняєш розмову з користувачем. Сформуй звіт для спеціалістів. Надай в повідомленні інформацію лише про стан чи проблему користувача"
            chat_log.append({"role": "user", "content": content})
            
            with ai.messages.stream(max_tokens=1024, messages=chat_log, model="claude-3-haiku-20240307", system=SYSTEM_PROMPT) as stream:
                for text in stream.text_stream:
                    report += text
                rep_id = str(db.сodecon.reports.insert_one({'text': report, 'rep_type':'Law'}).inserted_id)
                await websocket.send_json({"role": "end", "text": rep_id})
            break
        await websocket.send_json({"role": "finished", "text": msg_buf})