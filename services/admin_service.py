from sqlalchemy.orm import Session
from models.user_db import User, UserRole
from fastapi import HTTPException
from schemas.admin_ import AdminStats

def get_all_users(db: Session):
    return db.query(User).all()

def get_admin_stats(db: Session) -> AdminStats:
    return AdminStats(
        total_users=db.query(User).count(),
        total_partners=db.query(User).filter(User.role == UserRole.partner).count(),
        pending_kyc=db.query(User).filter(User.kyc_status == "pending").count()
    )
def require_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")

def approve_kyc(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.kyc_status == "approved":
        raise HTTPException(status_code=400, detail="User KYC already approved")

    user.kyc_status = "approved"
    user.tier += 1
    db.commit()
    db.refresh(user)

    return {"message": f"{user.full_name}'s KYC approved. Upgraded to Tier {user.tier}."}
