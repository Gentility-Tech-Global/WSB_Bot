from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated

PhoneNumberStr = Annotated[str, constr(min_length=10, max_length=15)]

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: PhoneNumberStr
    password: str
    kyc_method: Optional[str] ="BVN"
    bvn: Optional[str]
    nin: Optional[str]

class UserRegisterResponse(BaseModel):
    user_id: str
    message: str

class UserProfile(BaseModel):
    user_id: str
    full_name: Optional[str]
    email: Optional[EmailStr] 
    phone_number: Optional[str]
    address: Optional[str]

class UpdateUserProfile(BaseModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]