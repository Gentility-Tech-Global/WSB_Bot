import re
import uuid
from datetime import datetime
from typing import List
from schemas.transaction_ import (
    TransactionCreate,
    TransactionResponse,
    TransactionHistoryItem,
    TransactionHistoryResponse
)
from services.redis_service import get_data

ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}
transactions_db = []  # Simulated in-memory DB

def create_transaction(data: TransactionCreate) -> TransactionResponse:
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.utcnow()

    transaction_record = {
        "transaction_id": transaction_id,
        "sender_id": data.sender_id,
        "receiver_id": data.receiver_id,
        "amount": float(data.amount),
        "transaction_type": data.transaction_type,
        "status": "success",
        "timestamp": timestamp,
        "narration": data.narration
    }

    transactions_db.append(transaction_record)
    return TransactionResponse(**transaction_record)

def get_transaction_history(user_id: str) -> TransactionHistoryResponse:
    user_transactions: List[TransactionHistoryItem] = [
        TransactionHistoryItem(
            transaction_id=tx["transaction_id"],
            amount=tx["amount"],
            transaction_type=tx["transaction_type"],
            timestamp=tx["timestamp"],
            narration=tx.get("narration")
        )
        for tx in transactions_db
        if tx["sender_id"] == user_id or tx["receiver_id"] == user_id
    ]

    return TransactionHistoryResponse(user_id=user_id, transactions=user_transactions)

async def process_transfer(text: str, sender: str) -> str:
    try:
        amount_match = re.search(r"transfer (\d+)", text)
        account_match = re.search(r"to ([a-zA-Z]+) (\d{10})", text)

        if not (amount_match and account_match):
            return "Invalid format. Use: Transfer 2000 to GTB 0123456789"

        amount = float(amount_match.group(1))
        bank = account_match.group(1).upper()
        account_number = account_match.group(2)

        if bank not in ALLOWED_PARTNERS:
            return f"{bank} is not supported yet."

        # Simulated transfer
        return f"Transferring ₦{amount:,.2f} to {bank} {account_number}..."

    except Exception as e:
        return f"Error processing transfer: {str(e)}"
    

async def process_balance(sender: str, pin: str) -> str:
    # Dummy verification - replace with real authentication logic
    user_key = f"user:{sender}"
    user_data = await get_data(user_key)
    
    if not user_data:
        return "❌ User not found. Please onboard first using: Onboard John Doe, 08012345678, 0123456789, 1995-06-01"

    # Validate PIN - compare against stored one (mocked here)
    if str(user_data.get("pin")) != str(pin):
        return "❌ Incorrect PIN. Please try again."

    # Mock balance
    balance = user_data.get("balance", 15000)
    return f"💰 Your wallet balance is ₦{balance:,.2f}"
