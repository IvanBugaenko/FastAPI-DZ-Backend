from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OperationsResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int
    created_at: datetime
    created_by: int
    modified_at: Optional[datetime]
    modified_by: Optional[int]

    class Config:
        orm_mode = True
