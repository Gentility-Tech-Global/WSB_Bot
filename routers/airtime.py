from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AirtimeTopUp(BaseModel):
    phone_number: str
    amount: float

@router.post("/topup")
def top_up_airtime(data: AirtimeTopUp):
    return{"status": "Success", "Message": f"{data.amount} credited to {data.phone_number}"}