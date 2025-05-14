from fastapi import APIRouter, HTTPException
from schemas.account_balance_ import BalanceCheckRequest, BalanceCheckResponse
from services.account_balance_service import fetch_account_balance

router = APIRouter(prefix="/account", tags=["Account Balance"])

@router.post("/balance", response_model=BalanceCheckResponse)
async def check_balance(payload: BalanceCheckRequest):
    response = fetch_account_balance(payload)
    if response.status == "failed":
        raise HTTPException(status_code=403, detail=response.message)
    return response
