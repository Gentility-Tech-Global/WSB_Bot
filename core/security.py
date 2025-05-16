import os
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from core.config import settings
from dotenv import load_dotenv

load_dotenv()
FERNET_KEY = os.getenv("FERNET_SECRET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_SECRET_KEY not set in environment")

fernet = Fernet(settings.fernet_secret_key)

# Load secret key securely
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_super_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
