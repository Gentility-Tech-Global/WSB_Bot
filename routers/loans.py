from fastapi import APIRouter, HTTPException
from schemas.loan import LoanRequest, LoanResponse
from services.loan_service import process_loan_application

router = APIRouter(prefix="/loan", tags=["Loan Application"])

@router.post("/apply", response_model=LoanResponse)
async def apply_for_loan(payload: LoanRequest):
    response = process_loan_application(payload)
    if response.status == "failed":
        raise HTTPException(status_code=403, detail=response.message)
    return response
