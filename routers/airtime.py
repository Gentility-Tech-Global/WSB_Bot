from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AirtimeTopUp(BaseModel):
    phone_number: str
    amount: float

@router.post("/topup")
def top_up_airtime(data: AirtimeTopUp):
    # Simulate or call real API for airtime top-up
    return {
        "status": "success",
        "message": f"Airtime of NGN {data.amount} successfully recharged to {data.phone_number}"
    }
