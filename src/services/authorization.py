from src.core.settings import settings
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.users import Users
from src.models.schemas.users.users_request import UsersRequest
from datetime import datetime, timedelta
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.utils.hash import hash_password, check_password


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/authorization/authorize')


def get_current_user_info(token: str = Depends(oauth2_schema)) -> int:
    return AuthorizationService.verify_token(token)


class AuthorizationService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    
    @staticmethod
    def create_token(user_id, user_role) -> JwtToken:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': f'{user_id} {user_role}'
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

        return JwtToken(access_token=token)
    

    @staticmethod
    def verify_token(token: str) -> Optional[List]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')

        return payload.get('sub').split(' ')
    

    def register(self, user_schema: UsersRequest) -> None:
        user = Users(
                username = user_schema.username, 
                password_hashed = hash_password(user_schema.password_text), 
                role = user_schema.role, 
                created_by = user_schema.created_by
        )
        self.session.add(user)
        self.session.commit()


    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
                .query(Users)
                    .filter(Users.username == username)
                        .first()
        )

        if not user:
            return None
        if not check_password(password_text, user.password_hashed):
            return None
        
        return self.create_token(user.id, user.role)
