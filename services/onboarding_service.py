from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from passlib.hash import bcrypt

from schemas.onboard import UserRegister, UserProfile, UpdateUserProfile, UserRegisterResponse
from models.user_db import User
from models.wallet_db import Wallet
from utils.account import generate_account_number


ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}


def register_user(data: UserRegister, db: Session) -> UserRegisterResponse:
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


def get_user_profile(user_id: str, db: Session) -> UserProfile:
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


def update_user_profile(user_id: str, data: UpdateUserProfile, db: Session) -> UserProfile:
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
