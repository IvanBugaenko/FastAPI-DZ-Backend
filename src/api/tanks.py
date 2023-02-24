from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.tanks.tanks_request import TanksRequest
from src.models.schemas.tanks.tanks_response import TanksResponse
from services.tanks import TanksService
from src.api.utils.get_with_check import get_with_check
from src.services.authorization import get_current_user_info


router = APIRouter(
    prefix='/tanks',
    tags=['Tanks'],
    dependencies=[Depends(get_current_user_info)]
)


@router.get('/all', response_model=List[TanksResponse], name='Получение всех записей из таблицы "Tanks"')
def get(tanks_service: TanksService = Depends()):
    """
    Получение всех данных из таблицы Tanks
    """
    return tanks_service.all()


@router.get('/get/{tank_id}', response_model=TanksResponse, name='Получение одного резервуара')
def get(tank_id: int, tanks_service: TanksService = Depends()):
    """
    Получение данных из таблицы Tanks по id (с проверкой на наличие записи в БД)
    """
    return get_with_check(tank_id, tanks_service)


@router.post('/', response_model=TanksResponse, status_code=status.HTTP_201_CREATED, name='Добавление резервуара')
def add(tank_schema: TanksRequest, tanks_service: TanksService = Depends(), creating_id: int = Depends(get_current_user_info)):
    return tanks_service.add(tank_schema, creating_id[0])


@router.put('/{tank_id}', response_model=TanksResponse, name='Обновление информации о резервуаре')
def put(tank_id: int, tank_schema: TanksRequest, tanks_service: TanksService = Depends(), modifing_id: int = Depends(get_current_user_info)):
    """
    Обновление информации о резервуаре (с проверкой на наличие записи в БД)
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.update(tank_id, tank_schema, modifing_id[0])


@router.delete('/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удаление информации о резервуаре')
def delete(tank_id: int, tanks_service: TanksService = Depends()):
    """
    Удаление информации о резервуаре (с проверкой на наличие записи в БД)
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.delete(tank_id)


@router.get('/update_current_capacity/{tank_id}', response_model=TanksResponse, name='Изменение значения current_capacity')
def change(tank_id: int, new_capacuty: float, tanks_service: TanksService = Depends(), modifing_id: int = Depends(get_current_user_info)):
    """
    Обновление информации о поле current_capacity (с проверкой на наличие записи в БД)
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.update_current_capacity(tank_id, new_capacuty, modifing_id[0])
