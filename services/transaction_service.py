from sqlalchemy.orm import Session
from models.wallet_db import Wallet, TransactionLog
from core.config import settings
from fastapi import HTTPException
from datetime import datetime
from decimal import Decimal


def transfer_funds(sender_id: int, receiver_id: int, amount: Decimal, db: Session) -> dict:
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transfer amount")

    if amount > Decimal(settings.TRANSFER_LIMIT):
        raise HTTPException(status_code=400, detail=f"Transfer exceeds limit of {settings.TRANSFER_LIMIT}")

    # Fetch wallets
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == sender_id).first()
    receiver_wallet = db.query(Wallet).filter(Wallet.user_id == receiver_id).first()

    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")
    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Receiver wallet not found")

    if sender_wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Perform transfer
    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    # Log the transaction
    trnsaction = TransactionLog(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=Decimal(amount),
        timestamp=datetime.utcnow
    )
    # Optionally: Add to a transaction history model/table here

    db.commit()
    db.refresh(sender_wallet)
    db.refresh(receiver_wallet)

    return {
        "status": "success",
        "message": "Transfer successful",
        "data": {
            "from": sender_id,
            "to": receiver_id,
            "amount": str(amount),
            "sender_balance": str(sender_wallet.balance),
            "receiver_balance": str(receiver_wallet.balance),
            "timestamp": datetime.utcnow().isoformat()
        }
    }
