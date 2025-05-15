import uuid
from datetime import datetime
from typing import List
from schemas.transaction_ import (
    TransactionCreate,
    TransactionResponse,
    TransactionHistoryItem,
    TransactionHistoryResponse
)


# Simulated in-memory "database"
ALLOWED_PARTNERS = {"GTBank", "FunZ MFB"}
transactions_db = []

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
    user_transactions: List[TransactionHistoryItem] = []

    for tx in transactions_db:
        if tx["sender_id"] == user_id or tx["receiver_id"] == user_id:
            user_transactions.append(TransactionHistoryItem(
                transaction_id=tx["transaction_id"],
                amount=tx["amount"],
                transaction_type=tx["transaction_type"],
                timestamp=tx["timestamp"],
                narration=tx.get("narration")
            ))

    return TransactionHistoryResponse(
        user_id=user_id,
        transactions=user_transactions
    )
