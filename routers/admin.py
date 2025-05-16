from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user_db import User
from database.session import get_db
from dependencies.roles import require_role
from services import admin_service
from schemas.admin_ import UserSummary, AdminStats

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/only")
def admin_welcome(current_user: User = Depends(require_role("admin"))):
    return {"message": f"Welcome admin {current_user.full_name}"}


@router.get("/users", response_model=list[UserSummary])
def list_users(current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return admin_service.get_all_users(db)


@router.post("/kyc/approve/{user_id}")
def approve_kyc(user_id: int, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return admin_service.approve_kyc(user_id, db)


@router.get("/stats", response_model=AdminStats)
def admin_stats(current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return admin_service.get_admin_stats(db)
