from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Billpayment(BaseModel):
    Service_provider: str
    account_number: str
    amount: float

@router.post("/pay")
def pay_bill(payment: Billpayment):
    return {"status": "Success", "Message": f"Bill paid to {payment.service_provider}"}