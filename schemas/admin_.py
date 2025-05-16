from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSummary(BaseModel):
    id: int
    phone: str
    full_name: Optional[str]
    role: str
    kyc_status: str
    tier: int
    created_at: datetime

    class Config:
        from_attributes = True

class AdminStats(BaseModel):
    total_users: int
    total_partners: int
    pending_kyc: int
