from pydantic import BaseModel, Field
from typing import Optional

class LoanRequest(BaseModel):
    full_name: str
    bvn: str
    amount: float
    duration_months: int
    user_reference: str  # e.g., WhatsApp ID
    channel_partner: str = Field(..., description="e.g., GTBank, FunZ MFB")

class LoanResponse(BaseModel):
    status: str
    message: str
    loan_id: Optional[str] = None
