import time
import jwt
from fastapi import APIRouter, Request, Depends
from db import get_db
from config import CONFIG
from bson.objectid import ObjectId
from models import LoginUser
from pymongo import MongoClient
from mail import make_message, send_conf_mail_to
          
router = APIRouter(prefix="/auth")

@router.post('/login')
def login(request: Request, link_format: str, user: LoginUser):
    
    token = {}
    token["username"] = user.email.split("@")[0]
    token["rid"] = user.rid
    token["exp"] = time.time() + (60*10) # seconds * minutes
    encoded_jwt = jwt.encode(token, CONFIG.jwt_secret.get_secret_value(), algorithm="HS256")

    msg = make_message(link_format, encoded_jwt)
    sent = send_conf_mail_to(user.email, msg)
    return {"success": sent}


@router.get("/user")
def user(request: Request, key: str, db: MongoClient = Depends(get_db)):
    try:
        token = jwt.decode(key, CONFIG.jwt_secret.get_secret_value(), algorithms=["HS256"])
        codecon = db["codecon"]
        reports = codecon["reports"]
        report = reports.find_one(ObjectId(token["rid"]))
        print(report)
        if time.time() < token["exp"]:
            return {"success": True, "username": token["username"], "type": report["rep_type"]}
        else: raise Exception
    except Exception as E:
        print("EXCEPTION:", E)
        return {"success": False, "username": None}
