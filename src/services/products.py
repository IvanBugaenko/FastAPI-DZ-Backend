from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.products import Products
from src.models.schemas.products.products_request import ProductsRequest
from datetime import datetime


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def all(self) -> List[Products]:
        products = (
            self.session
                .query(Products)
                    .order_by(Products.id.asc())
                        .all()
        )

        return products
    

    def get(self, product_id: int) -> Products:
        product = (
            self.session
                .query(Products)
                    .filter(Products.id == product_id)
                        .first()
        )

        return product


    def add(self, products_schema: ProductsRequest, creating_id: int) -> Products:
        product = Products(**products_schema.dict())
        product.created_by = creating_id
        self.session.add(product)
        self.session.commit()

        return product
    

    def update(self, product_id: int, products_schema: ProductsRequest, modifying_id: int) -> Products:
        product = self.get(product_id)
        for field, value in products_schema:
            if value and value != 0:
                setattr(product, field, value)

        product.modified_by = modifying_id
        product.modified_at = datetime.now()

        self.session.commit()

        return product
    

    def delete(self, product_id: int) -> None:
        product = self.get(product_id)
        self.session.delete(product)
        self.session.commit()
