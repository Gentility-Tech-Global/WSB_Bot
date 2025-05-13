from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.security import verify_password, create_access_token, hash_password
from models.user_db import User
from sqlalchemy.orm import Session
from database.session import SessionLocal, get_db
from schemas.user import UserCreate, Token
from pydantic import BaseModel


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="app/v1/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
# Mock database (Replace with real DB lookup)
class RegisterRequest(BaseModel):
   phone: str
   full_name: str
   bvn: str
   password: str
   role: str ="user"


@router.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.phone, "role": user.role.name})
    return {"access_token": token, "token_type": "bearer"}



@router.post("/register")
def register_user(req: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.phone == req.phone).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    user = User(
        phone=req.phone,
        fullname=req.full_name,
        bvn=req.bvn,
        hashed_password=hash_password(req.password),
        role=req.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registration successful", "user_id": user.id}

@router.post("/login")
def login(phone: str, password: str, db: Session = Depends(get_db)):
          user = db.query(User).filter(User.phone == phone).first()
          if not user or not verify_password(password, user.hashed_password):
               raise HTTPException(status_code=401, detail="Invalid credentials")
          
          access_token = create_access_token(data={"sub": str(user.id)})
          return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get current user
from jose import JWTError
from core.security import decode_token

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.phone == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user