import secrets
from mail import make_message, send_conf_mail_to
from db import get_db
from config import CONFIG
from models import LoginUser, ValidToken
from fastapi import APIRouter, Depends, Request, HTTPException 
from pymongo import MongoClient
import jwt
            

router = APIRouter(prefix="/auth")


@router.post('/login')
def login(request: Request, link_format: str, user: LoginUser):
    
    token = {}
    token["username"] = user.email.split("@")[0]
    encoded_jwt = jwt.encode(token, CONFIG.jwt_secret.get_secret_value(), algorithm="HS256")

    msg = make_message(link_format, encoded_jwt)
    sent = send_conf_mail_to(user.email, msg)
    return {"success": msg}


@router.get("/user")
def user(request: Request, key: str):
    try:
        token = jwt.decode(key, CONFIG.jwt_secret.get_secret_value(), algorithms=["HS256"])
        validated_token = ValidToken.parse_obj(token)
        return {"success": True, "username": token["username"]}
    except:
        return {"success": False, "username": None}
    # session_mgr = request.state.session
    # session = session_mgr.get_session()
    # token = session.get("token", None)
    # session["is_authenticated"] = True  -- При успіху

