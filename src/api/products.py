from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.products.products_request import ProductsRequest
from src.models.schemas.products.products_response import ProductsResponse
from services.products import ProductsService
from src.api.utils.get_with_check import get_with_check
from src.services.authorization import get_current_user_info


router = APIRouter(
    prefix='/products',
    tags=['Products'],
    dependencies=[Depends(get_current_user_info)]
)


@router.get('/all', response_model=List[ProductsResponse], name='Получение всех записей из таблицы "Products"')
def get(products_service: ProductsService = Depends()):
    """
    Получение всех данных из таблицы Products
    """
    return products_service.all()


@router.get('/get/{product_id}', response_model=ProductsResponse, name='Получение одного продукта')
def get(product_id: int, products_service: ProductsService = Depends()):
    """
    Получение данных из таблицы Products по id (с проверкой на наличие записи в БД)
    """
    return get_with_check(product_id, products_service)


@router.post('/', response_model=ProductsResponse, status_code=status.HTTP_201_CREATED, name='Добавление продукта')
def add(product_schema: ProductsRequest, products_service: ProductsService = Depends(), creating_id: int = Depends(get_current_user_info)):
    return products_service.add(product_schema, creating_id[0])


@router.put('/{product_id}', response_model=ProductsResponse, name='Обновление информации о продукте')
def put(product_id: int, product_schema: ProductsRequest, products_service: ProductsService = Depends(), modifing_id: int = Depends(get_current_user_info)):
    """
    Обновление информации о продуктах (с проверкой на наличие записи в БД)
    """
    get_with_check(product_id, products_service)
    return products_service.update(product_id, product_schema, modifing_id[0])


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удаление информации о продукте')
def delete(product_id: int, products_service: ProductsService = Depends()):
    """
    Удаление информации о продукте (с проверкой на наличие записи в БД)
    """
    get_with_check(product_id, products_service)
    return products_service.delete(product_id)