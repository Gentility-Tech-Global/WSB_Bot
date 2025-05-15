from pydantic import BaseModel, constr, condecimal
from typing import Optional, List, Annotated
from datetime import datetime


TransferAmt = Annotated[int, condecimal(gt=0)]
TransactionType =Annotated[str, constr(pattern="^(transfer|credit|debit)$")]

class TransactionCreate(BaseModel):
    sender_id: str
    receiver_id: str
    amount: TransferAmt
    transaction_type: TransactionType
    narration: Optional[str] = None

class TransactionResponse(BaseModel):
    transaction_id: str
    sender_id: str
    receiver_id: str
    amount: float
    transaction_type: str
    status: str
    timestamp: datetime
    narration: Optional[str]

class TransactionHistoryItem(BaseModel):
    transaction_id: str
    amount: float
    transaction_type: str
    timestamp: datetime
    narration: Optional[str]

class TransactionHistoryResponse(BaseModel):
    user_id: str
    transactions: List[TransactionHistoryItem]
