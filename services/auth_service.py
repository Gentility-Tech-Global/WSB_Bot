from schemas.auth_ import UserLogin, UserRegister, Token, RefreshTokenRequest
from sqlalchemy.orm import Session
from models.user_db import User
from utils.hash_utils import hash_password, verify_password
from core.security import create_access_token, create_refresh_token, decode_token
from fastapi import HTTPException

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

def validate_partner(channel_partner: str):
    if channel_partner not in ALLOWED_PARTNERS:
        raise HTTPException(status_code=403, detail=f"Unauthorized partner: {channel_partner}")


def register_user(data: UserRegister, db: Session):
    if db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")

    new_user = User(
        phone=data.phone,
        full_name=data.full_name,
        bvn=data.bvn,
        date_of_birth=data.date_of_birth,
        hashed_password=hash_password(data.password),
        role=data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registration successful", "user_id": new_user.id}


def login_user(data: UserLogin, db: Session) -> Token:
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "role": user.role})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def refresh_access_token(request: RefreshTokenRequest) -> Token:
    payload = decode_token(request.refresh_token)
    phone = payload.get("sub")
    access_token = create_access_token({"sub": phone})
    new_refresh_token = create_refresh_token({"sub": phone})
    return Token(access_token=access_token, refresh_token=new_refresh_token)
