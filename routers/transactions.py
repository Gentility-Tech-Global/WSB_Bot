from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from routers.auth import get_current_user
from models.user_db import User

router = APIRouter()

class TransferRequest(BaseModel):
    sender_account: str
    sender_bank_name: str
    receiver_account: str
    receiver_bank_name: str
    amount: float

@router.post("/send")
async def send_money(request: TransferRequest, user: User = Depends(get_current_user)):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    # TODO: Implement real balance check
    return {
        "status": "Success", 
        "Message": f"{user.full_name}, your transfer of #{request.amount} is completed"
    }
