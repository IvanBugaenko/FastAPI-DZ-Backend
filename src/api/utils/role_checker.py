from fastapi import Depends, HTTPException, status
from typing import List
from src.services.authorization import AuthorizationService, get_current_user_info


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles


    def __call__(self, user_info: AuthorizationService = Depends(get_current_user_info)):
        if  user_info[1] not in self.allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
