from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class KYCRequest(BaseModel):
    full_name: str
    phone_number: str
    bvn: str
    date_of_birth: str

@router.post("/register")
def register_user(data: KYCRequest):
    if len(data.bvn) != 11:
        raise HTTPException(status_code=400, detail="Invalid BVN")
    return {"status": "success", "account_number": "1234567890"}
