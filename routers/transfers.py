from fastapi import APIRouter, HTTPException
from schemas.transaction_ import (
    TransactionCreate,
    TransactionResponse,
    TransactionHistoryResponse
)
from services.transaction_service import (
    create_transaction,
    get_transaction_history
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/create", response_model=TransactionResponse)
def initiate_transaction(transaction: TransactionCreate):
    try:
        return create_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}", response_model=TransactionHistoryResponse)
def fetch_transaction_history(user_id: str):
    try:
        return get_transaction_history(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
