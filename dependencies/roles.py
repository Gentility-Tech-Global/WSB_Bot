# dependencies/roles.py
from fastapi import Depends, HTTPException
from starlette import status
from routers.auth import get_current_user  # Be cautious here

def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if str(user.role) != role:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient privileges")
        return user
    return role_checker
