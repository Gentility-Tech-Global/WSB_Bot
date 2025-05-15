from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_db import User
from schemas.kyc_ import KYCUpgradeRequest

ALLOWED_PARTNERS = {"FunZ MFB", "GTBank", ...}

def validate_partner(partner: str):
    if partner not in ALLOWED_PARTNERS:
        raise HTTPException(status_code=403, detail=f"Unauthorized partner: {partner}")
    

def process_kyc_upgrade(req: KYCUpgradeRequest, user: User, db: Session):
    if req.tier <= user.tier:
        raise HTTPException(status_code=400, detail="You already have this tier or higher")
    
    # Validate tier requirements
    if req.tier == 2:
        if not req.nin or not req.document_url:
            raise HTTPException(status_code=422, detail="NIN and NIN slip are required for Tier 2")
        user.nin = req.nin
        user.nin_url = req.document_url

    elif req.tier == 3:
        if not req.address or not req.document_url:
            raise HTTPException(status_code=422, detail="Address and utility bill are required for Tier 3")
        user.address = req.address
        user.address_proof_url = req.document_url

    user.kyc_status = "pending"
    db.commit()
    db.refresh(user)

    return {"message": f"KYC upgrade to Tier {req.tier} submitted. Awaiting admin review."}