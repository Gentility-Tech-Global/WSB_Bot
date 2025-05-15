from pydantic import BaseModel, Field
from typing import Literal

class KYCUpgradeRequest(BaseModel):
    tier: Literal[2, 3] = Field(..., description="Upgrade to Tier 2 or Tier 3 only")
    document_url: str = Field(..., description="NIN or Address Proof URL")
    nin: str | None = Field(None, description="Required for Tier 2")
    address: str | None = Field(None, description="Required for Tier 3")
    channel_partner: str = Field(..., description="Source of request: GTBank, FunZ MFB, etc.")
    