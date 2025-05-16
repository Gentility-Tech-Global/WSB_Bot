from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.otp_db import UserOTP
from datetime import datetime


async def verify_otp(user_id: int, otp: str, db: Session):
    record = db.query(UserOTP).filter(UserOTP.user_id == user_id).first()

    if not record or record.otp_code != otp:
        raise HTTPException(status_code=401, detail="Invalide Otp")
    if datetime.utcnow() > record.expires_at:
        raise HTTPException(status_code=410, detail="OTP expired")
    
    db.delete(record)
    db.commit()

    return{"message": "✅ OTP verified successfully"}