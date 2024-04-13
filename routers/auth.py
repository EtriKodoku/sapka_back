import time
import jwt
from fastapi import APIRouter, Request
from db import get_db
from config import CONFIG
from models import LoginUser
from mail import make_message, send_conf_mail_to
          
router = APIRouter(prefix="/auth")

@router.post('/login')
def login(request: Request, link_format: str, user: LoginUser):
    
    token = {}
    token["username"] = user.email.split("@")[0]
    token["exp"] = time.time() + (60*10) # seconds * minutes
    encoded_jwt = jwt.encode(token, CONFIG.jwt_secret.get_secret_value(), algorithm="HS256")

    msg = make_message(link_format, encoded_jwt)
    sent = send_conf_mail_to(user.email, msg)
    return {"success": sent}


@router.get("/user")
def user(request: Request, key: str):
    try:
        token = jwt.decode(key, CONFIG.jwt_secret.get_secret_value(), algorithms=["HS256"])
        if time.time() < token["exp"]:
            return {"success": True, "username": token["username"]}
        else: raise Exception
    except:
        return {"success": False, "username": None}
