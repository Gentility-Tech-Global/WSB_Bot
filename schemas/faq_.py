from pydantic import BaseModel, Field
from typing import List, Optional

class FAQ(BaseModel):
    id: int
    question: str
    answer: str

class FAQResponse(BaseModel):
    status: str
    data: Optional[List[FAQ]] = None
    message: str

class PartnerRequest(BaseModel):
    channel_partner: str = Field(..., description="e.g., GTBank, FunZ MFB")
    