from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated
from datetime import date

PhoneNumberStr = Annotated[str, constr(min_length=10, max_length=15)]

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: PhoneNumberStr
    password: str
    date_of_birth: date
    kyc_method: Optional[str] ="BVN"
    bvn: Optional[str]
    nin: Optional[str]
    partner: str

def validate_partner(self):
        allowed_partners = {"GTBank", "FunZ MFB", "UBA"}
        if self.partner not in allowed_partners:
            raise ValueError("Invalid partner. Only authorized partners can onboard users.")
        

class UserRegisterResponse(BaseModel):
    user_id: str
    message: str

class UserProfile(BaseModel):
    user_id: str
    full_name: Optional[str]
    phone_number: Optional[str]
    date_of_birth: date
    bvn: Optional[str]
    role: Optional[str]
    email: Optional[EmailStr] 
    address: Optional[str]

class UpdateUserProfile(BaseModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    date_of_birth: date
    bvn: Optional[str]
    address: Optional[str]
    role: Optional[str]