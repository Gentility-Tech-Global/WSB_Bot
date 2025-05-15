from fastapi import APIRouter, Depends, HTTPException
from models.user_db import User
from database.session import get_db
from routers.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/only")
def admin_route(user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": f"Welcome admin {user.full_name}"}


@router.get("/users")
def list_users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(User).all()


@router.post("/admin/kyc/approve/{user_id}")
def approve_kyc(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    
    kyc_user = db.query(User).filter(User.id == user_id).first()
    if not kyc_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    kyc_user.kyc_status = "approved"
    kyc_user.tier +=1
    db.commit()
    return {"message": f"User{kyc_user.full_name} upgrade to Tier {kyc_user.tier}"}