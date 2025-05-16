from fastapi import Depends, HTTPException
from starlette import status
from routers.auth import get_current_user  
from typing import List, Union

def require_role(allowed_roles: Union[str, List[str]]):
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def role_checker(user=Depends(get_current_user)):
        if str(user.role) not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Insufficient privileges"
            )
        return user
    return role_checker
