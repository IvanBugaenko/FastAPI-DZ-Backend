from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.users import Users
from src.models.schemas.users.users_request import UsersRequest
from datetime import datetime
from src.services.utils.hash import hash_password


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def all(self) -> List[Users]:
        users = (
            self.session
                .query(Users)
                    .order_by(Users.id.asc())
                        .all()
        )

        return users
    
    def get(self, user_id: int) -> Users:
        user = (
            self.session
                .query(Users)
                    .filter(Users.id == user_id)
                        .first()
        )

        return user


    def add(self, user_schema: UsersRequest, creating_id: int) -> Users:
        user = Users(
                username = user_schema.username, 
                password_hashed = hash_password(user_schema.password_text), 
                role = user_schema.role, 
                created_by = creating_id
        )
        self.session.add(user)
        self.session.commit()

        return user
    

    def update(self, user_id: int, user_schema: UsersRequest, modifying_id: int) -> Users:
        user = self.get(user_id)
        for field, value in user_schema:
            if value and value != 0:
                setattr(user, field, value)

        if len(str(user_schema.password_text)) > 0:
            setattr(user, user.password_hashed, hash_password(user_schema.password_text))

        user.modified_by = modifying_id
        user.modified_at = datetime.now()

        self.session.commit()

        return user
    

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()

