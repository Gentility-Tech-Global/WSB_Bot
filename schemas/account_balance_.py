from pydantic import BaseModel, Field
from typing import Optional

class BalanceCheckRequest(BaseModel):
    user_id: str = Field(..., description="Internal user ID or wallet ID")
    channel_partner: str = Field(..., description="e.g., GTBank, FunZ MFB")

class BalanceCheckResponse(BaseModel):
    status: str
    balance: Optional[float] = None
    currency: Optional[str] = None
    message: str
