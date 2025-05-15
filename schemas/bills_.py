from pydantic import BaseModel, Field
from typing import Optional

class BillPaymentRequest(BaseModel):
    bill_type: str  # e.g., "electricity", "tv", "internet"
    customer_id: str  # Meter Number, IUC, etc.
    amount: float
    provider: str  # e.g., "IKEDC", "DSTV", "SMILE"
    user_reference: str  # WhatsApp phone, or internal identifier
    channel_partner: str = Field(..., description="e.g., GTBank, FunZ MFB")

class BillPaymentResponse(BaseModel):
    status: str
    message: str
    transaction_id: Optional[str] = None
