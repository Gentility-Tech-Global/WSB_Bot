from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from passlib.hash import bcrypt

from schemas.onboard import (
    UserRegister,
    UserProfile,
    UpdateUserProfile,
    UserRegisterResponse
)
from models.user_db import User
from models.wallet_db import Wallet
from utils.account import generate_account_number
from database.session import SessionLocal
from utils.otp_utils import save_otp
from utils.whatsapp_utils import send_whatsapp_otp
import re


# Define which partners are allowed to onboard users
ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}

async def register_user(data: UserRegister, db: Session) -> UserRegisterResponse:
    if data.partner not in ALLOWED_PARTNERS:
        raise HTTPException(status_code=403, detail="Partner not authorized for onboarding")

    existing_user = db.query(User).filter(User.phone == data.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists with this phone number")

    hashed_password = bcrypt.hash(data.password)

    new_user = User(
        full_name=data.full_name,
        phone=data.phone_number,
        hashed_password=hashed_password,
        date_of_birth=data.date_of_birth,
        bvn=data.bvn,
        role=data.role,
        kyc_status="pending",
        partner=data.partner
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    account_number = generate_account_number(str(new_user.id))

    wallet = Wallet(user_id=new_user.id, balance=0.0)
    db.add(wallet)
    db.commit()

    return UserRegisterResponse(
        user_id=str(new_user.id),
        message=f"Onboarding successful. Your account number is {account_number}"
    )

async def get_user_profile(user_id: str, db: Session) -> UserProfile:
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserProfile(
        user_id=str(user.id),
        full_name=user.full_name,
        phone_number=user.phone,
        date_of_birth=user.date_of_birth,
        bvn=user.bvn,
        role=user.role,
        email=None,
        address=None
    )

async def update_user_profile(user_id: str, data: UpdateUserProfile, db: Session) -> UserProfile:
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.full_name:
        user.full_name = data.full_name
    if data.phone_number:
        user.phone = data.phone_number
    if data.date_of_birth:
        user.date_of_birth = data.date_of_birth
    if data.bvn:
        user.bvn = data.bvn
    if data.role:
        user.role = data.role

    db.commit()

    return UserProfile(
        user_id=str(user.id),
        full_name=user.full_name,
        phone_number=user.phone,
        date_of_birth=user.date_of_birth,
        bvn=user.bvn,
        role=user.role,
        email=None,
        address=None
    )

async def onboard_user(text: str, sender: str) -> str:
    try:
        data_match = re.findall(
            r"([A-Za-z\s]+),\s*(\d{11}),\s*(\d{10,11}),\s*(\d{4}-\d{2}-\d{2})", text
        )
        if not data_match:
            return (
                "❌ Invalid format.\n"
                "✅ Use: Onboard John Doe, 08012345678, 2233445566, 1995-06-01"
            )

        full_name, phone, bvn, dob = data_match[0]

        # Use default values for WhatsApp onboarding
        password = "default@123"
        partner = "FunZ MFB"

        user_data = UserRegister(
            full_name=full_name.strip(),
            phone_number=phone.strip(),
            password=password,
            bvn=bvn.strip(),
            date_of_birth=dob.strip(),
            partner=partner,
            role="customer"
        )

        db = SessionLocal()
        try:
            response = await register_user(user_data, db)
            otp = save_otp(int(response.user_id), db)
            send_whatsapp_otp(phone.strip(), otp)
        finally:
            db.close()

        return (
            f"🎉 Hello {full_name.strip()}!\n"
            f"Your onboarding was successful.\n"
            f"🧾 Account Number: {response.message.split()[-1]}\n"
            f"🔑 Default Password: {password} (please change it)."
            f"📲 A 6-digit OTP has been sent to your WhatsApp for verification."
        )

    except HTTPException as http_err:
        return f"⚠️ {http_err.detail}"

    except Exception as e:
        return f"❌ Failed to onboard due to: {str(e)}"
