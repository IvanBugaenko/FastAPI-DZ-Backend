from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ProductsRequest(BaseModel):
    name: Optional[str]
