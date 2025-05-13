from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoanRequest(BaseModel):
    account_number: str
    amount: float
    duration_months: int

@router.post("/apply")
def apply_loan(loan: LoanRequest):
    return {"status": "success", "message": "Loan application received"}