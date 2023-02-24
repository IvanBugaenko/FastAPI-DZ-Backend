from fastapi import APIRouter, Depends, status
from typing import List
from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.users.users_response import UsersResponse
from services.users import UsersService
from src.api.utils.get_with_check import get_with_check
from src.api.utils.role_checker import RoleChecker
from src.services.authorization import get_current_user_info


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[Depends(RoleChecker(['admin']))]
)


@router.get('/all', response_model=List[UsersResponse], name='Получение всех записей из таблицы "Users"')
def get(users_service: UsersService = Depends()):
    """
    Получение всех данных из таблицы Users
    """
    return users_service.all()


@router.get('/get/{user_id}', response_model=UsersResponse, name='Получение одного пользователя')
def get(user_id: int, users_service: UsersService = Depends()):
    """
    Получение данных из таблицы Users по id (с проверкой на наличие записи в БД)
    """
    return get_with_check(user_id, users_service)


@router.post('/', response_model=UsersResponse, status_code=status.HTTP_201_CREATED, name='Добавление пользователя')
def add(user_schema: UsersRequest, users_service: UsersService = Depends(), creating_id: int = Depends(get_current_user_info)):
    return users_service.add(user_schema, creating_id[0])


@router.put('/{user_id}', response_model=UsersResponse, name='Обновление информации о пользователе')
def put(user_id: int, user_schema: UsersRequest, users_service: UsersService = Depends(), modifing_id: int = Depends(get_current_user_info)):
    """
    Обновление информации о пользователе (с проверкой на наличие записи в БД)
    """
    get_with_check(user_id, users_service)
    return users_service.update(user_id, user_schema, modifing_id[0])


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удаление информации о пользователе')
def delete(user_id: int, users_service: UsersService = Depends()):
    """
    Удаление информации о пользователе (с проверкой на наличие записи в БД)
    """
    get_with_check(user_id, users_service)
    return users_service.delete(user_id)
