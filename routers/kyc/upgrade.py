from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Literal
from routers.auth import get_current_user
from models.user_db import User
from database.session import get_db

router = APIRouter(prefix="/kyc", tags=["KYC"])

class KYCUpgradeRequest(BaseModel):
    tier: Literal[2, 3] = Field(..., description="Upgrade to Tier 2 or 3 only")
    document_url: str = Field(..., description="URL of uploaded NIN slip or address proof")

@router.post("/upgrade")
def upgrade_kyc(
    req: KYCUpgradeRequest,
    db: Session = Depends (get_db), 
    current_user: User = Depends(get_current_user)
):
    if req.tier <= current_user.tier:
        raise HTTPException(status_code=400, detail="You already have this tier or higher")
    
    if req.tier == 2:
        current_user.nin_url = req.document_url
    elif req.tier == 3:
        current_user.address_proof_url = req.document_url

    current_user.kyc_status = "pending"
    db.commit()
    db.refresh(current_user)

    return {"message": f"KYC Tier {req.tier} submitted for approval. Please await admin review."}