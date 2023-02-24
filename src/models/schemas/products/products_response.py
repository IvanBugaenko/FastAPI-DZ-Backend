from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductsResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: int
    modified_at: Optional[datetime]
    modified_by: Optional[int]

    class Config:
        orm_mode = True
