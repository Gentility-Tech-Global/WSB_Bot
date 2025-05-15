from fastapi import APIRouter, Depends, HTTPException
from models.user_db import User
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.auth_ import UserRegister, UserLogin, Token, PartnerAuth
from services.auth_service import register_user, login_user, validate_partner

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(data: UserRegister, partner: PartnerAuth, db: Session = Depends(get_db)):
    validate_partner(partner.channel_partner)
    return register_user(data, db)

@router.post("/login", response_model=Token)
def login(data: UserLogin, partner: PartnerAuth, db: Session = Depends(get_db)):
    validate_partner(partner.channel_partner)
    return login_user(data, db)


# Dependency to get current user
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.phone == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user