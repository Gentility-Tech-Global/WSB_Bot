from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    partner = "partner"

class UserinDB(BaseModel):
    id: int
    phone: str
    full_name: str
    role: UserRole
    kyc_status: str
    tier: int

class Config:
    from_attributes = True

class User(BaseModel):
    phone: str
    bvn: str
    full_name: str | None = None

class UserCreate(User):
    password: str
    role: UserRole = UserRole.user

class UserOut(User):
    role: UserRole

class UserinDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
