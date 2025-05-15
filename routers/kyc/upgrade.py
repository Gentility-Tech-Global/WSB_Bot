from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.kyc_ import KYCUpgradeRequest
from services.kyc_service import process_kyc_upgrade, validate_partner
from routers.auth import get_current_user
from models.user_db import User

router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.post("/upgrade")
def upgrade_kyc(
    req: KYCUpgradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    validate_partner(req.channel_partner)
    return process_kyc_upgrade(req, current_user, db)