from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserLogin(BaseModel):
    phone: str
    password: str

class UserRegister(BaseModel):
    phone: str
    full_name: str
    bvn: str
    password: str
    role: str = "user"
    date_of_birth: str

class PartnerAuth(BaseModel):
    channel_partner: str = Field(..., description="Name of the platform (e.g., GTBank, FunZ MFB)")