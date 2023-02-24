from fastapi import FastAPI, Depends
from src.api.base_router import router
from db.db import Session
from src.models.users import Users
from src.core.settings import settings
from src.services.authorization import AuthorizationService


tags_dict = [
    {
        'name': 'operations',
        'description': 'Информация об операциях с резервуарами'
    },
    {
        'name': 'users',
        'description': 'Информация об операциях с пользователями и регистрация'
    },
    {
        'name': 'tanks',
        'description': 'Информация о резервуарах'
    },
    {
        'name': 'products',
        'description': 'Информация о продуктах'
    },
    {
        'name': 'authorization',
        'description': 'Авторизация и регистрация пользователей'
    },
]


def check() -> None:
    with Session.begin() as session:
        user = (
            session
                .query(Users)
                    .filter(Users.role == 'admin')
                        .first()
        )
        if not user:
            admin = Users(
                id = 1,
                username = settings.admin_login, 
                password_hashed = AuthorizationService.hash_password(settings.admin_password), 
                role = 'admin', 
                created_by = 1
            )
            session.add(admin)
            session.commit()


app = FastAPI(
    title='Домашнее задание по FastApi',
    description='Пробуем апишечки :)',
    version='0.0.1',
    openapi_tags=tags_dict,
    on_startup=[check]
)


app.include_router(router)
