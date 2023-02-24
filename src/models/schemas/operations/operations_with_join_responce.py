from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.models.schemas.tanks.tanks_response import TanksResponse
from src.models.schemas.products.products_response import ProductsResponse


class OperationsWithJoinResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    tank: TanksResponse
    product_id: int
    product1: ProductsResponse
    created_at: datetime
    created_by: int
    modified_at: Optional[datetime]
    modified_by: Optional[int]

    class Config:
        orm_mode = True
