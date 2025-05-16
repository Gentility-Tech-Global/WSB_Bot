import random
from datetime import datetime, timedelta
from models.otp_db import UserOTP
from sqlalchemy.orm import Session

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def save_otp(user_id: int, db: Session) -> str:
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    db.query(UserOTP).filter(UserOTP.user_id == user_id).delete()
    db.add(UserOTP(user_id=user_id, otp_code=otp, expires_at=expires_at))
    db.commit()
    return otp
