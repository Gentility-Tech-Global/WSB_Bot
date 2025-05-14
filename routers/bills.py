from fastapi import APIRouter, HTTPException
from schemas.bills_ import BillPaymentRequest, BillPaymentResponse
from services.bills_service import process_bill_payment

router = APIRouter(prefix="/bills", tags=["Bills Payment"])

@router.post("/pay", response_model=BillPaymentResponse)
async def pay_bill(payload: BillPaymentRequest):
    response = process_bill_payment(payload)
    if response.status == "failed":
        raise HTTPException(status_code=403, detail=response.message)
    return response
