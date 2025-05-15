from fastapi import APIRouter, HTTPException, Depends
from schemas.onboard import UserRegister, UserProfile, UserRegisterResponse, UpdateUserProfile
from services.onboarding_service import register_user, get_user_profile, update_user_profile
from database.session import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post("/register", response_model=UserRegisterResponse)
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    try:
        return register_user(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/profile/{user_id}", response_model=UserProfile)
def profile(user_id: str, db: Session = Depends(get_db)):
    try:
        return get_user_profile(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/profile/{user_id}", response_model=UserProfile)
def update_profile(user_id: str, data: UpdateUserProfile, db: Session = Depends(get_db)):
    try:
        return update_user_profile(user_id, data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))