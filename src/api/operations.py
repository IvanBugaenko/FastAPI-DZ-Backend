from fastapi import APIRouter, Depends, status
from typing import List
from src.models.schemas.operations.operations_request import OperationsRequest
from src.models.schemas.operations.operations_response import OperationsResponse
from src.models.schemas.operations.operations_with_join_responce import OperationsWithJoinResponse
from services.operations import OperationsService
from src.services.tanks import TanksService
from src.services.authorization import get_current_user_info
from src.api.utils.get_with_check import get_with_check
from datetime import datetime
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix='/operations',
    tags=['Operations'],
    dependencies=[Depends(get_current_user_info)]
)


@router.get('/all', response_model=List[OperationsWithJoinResponse], name='Получение всех записей из таблицы "Operations"')
def get(operations_service: OperationsService = Depends()):
    """
    Получение всех данных из таблицы Operations (включая данные из таблиц Tanks и Products)
    """
    return operations_service.all()


@router.get('/get/{operation_id}', response_model=OperationsResponse, name='Получение одной операции')
def get(operation_id: int, operations_service: OperationsService = Depends()):
    """
    Получение данных из таблицы Operations по id (с проверкой на наличие записи в БД)
    """
    return get_with_check(operation_id, operations_service)


@router.post('/', response_model=OperationsResponse, status_code=status.HTTP_201_CREATED, name='Добавление операции')
def add(operation_schema: OperationsRequest, operations_service: OperationsService = Depends(), creating_id: int = Depends(get_current_user_info)):
    return operations_service.add(operation_schema, creating_id[0])


@router.put('/{operation_id}', response_model=OperationsResponse, name='Обновление информации об операции')
def put(operation_id: int, operation_schema: OperationsRequest, operations_service: OperationsService = Depends(), modifing_id: int = Depends(get_current_user_info)):
    """
    Обновление информации об операциях (с проверкой на наличие записи в БД)
    """
    get_with_check(operation_id, operations_service)
    return operations_service.update(operation_id, operation_schema, modifing_id[0])


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удаление информации об опарации')
def delete(operation_id: int, operations_service: OperationsService = Depends()):
    """
    Удаление информации об операции (с проверкой на наличие записи в БД)
    """
    get_with_check(operation_id, operations_service)
    return operations_service.delete(operation_id)


@router.get('/get_by_tank_id/{tank_id}', response_model=list[OperationsResponse], name='Получение всех операций по названию резервуара')
def get_by_tank(tank_id: int, operations_service: OperationsService = Depends(), tank_service: TanksService = Depends()):
    get_with_check(tank_id, tank_service)
    return operations_service.find_by_tank(tank_id)


@router.get('/download', response_model=List[OperationsResponse], name='Формирование отчета')
def report(tank_id: int, product_id: int, date_start: datetime, date_end: datetime, operations_service: OperationsService = Depends()):
    """
    Формирование отчета в формате csv по пользовательским данным
    """
    report = operations_service.download(tank_id, product_id, date_start, date_end)
    return StreamingResponse(report, media_type='text/csv', 
                             headers={
                                'Content-Disposition': 'attachment; filename=report.csv'
                             })
