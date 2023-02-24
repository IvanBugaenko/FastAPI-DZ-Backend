from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TanksRequest(BaseModel):
    name: Optional[str]
    max_capacity: Optional[float]
    current_capacity: Optional[float]
    product_id: Optional[int]
