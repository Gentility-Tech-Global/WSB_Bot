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
    # Check if user already exists by phone or email
    existing_user = db.query(User).filter(User.phone == data.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists with this phone number")

    # Hash the password
    hashed_password = bcrypt.hash(data.password)

    # Create new user record
    new_user = User(
        full_name=data.full_name,
        phone=data.phone_number,
        hashed_password=hashed_password,
        date_of_birth=data.date_of_birth,
        kyc_status="pending",
        partner=data.partner
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate account number based on new user ID
    account_number = generate_account_number(str(new_user.id))

    # Create wallet for the new user
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
        email=None,  # Add email field in User model if needed
        address=None  # Add address field in User model if needed
    )


def update_user_profile(user_id: str, data: UpdateUserProfile, db: Session) -> UserProfile:
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.full_name:
        user.full_name = data.full_name
    if data.phone_number:
        user.phone = data.phone_number
    # Add additional fields as needed
    db.commit()

    return UserProfile(
        user_id=str(user.id),
        full_name=user.full_name,
        phone_number=user.phone,
        email=None,
        address=None
    )
