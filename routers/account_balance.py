from fastapi import APIRouter, Depends
from routers.auth import get_current_user
from schemas.user import UserinDB

router = APIRouter()

@router.get("/balance/{account_number}")
def get_balance(account_number: str):
    # Mocked logic
    balance = 12400.50
    return {"Account_number": account_number, "Balance": balance}


@router.get("/secure/balance")
def check_balance(user=Depends(get_current_user)):
    return {"message": f"Hello {user.full_name}, here's your balance."}

@router.get("/secure-data")
def secure_endpoint(current_user: UserinDB = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.full_name}"}
