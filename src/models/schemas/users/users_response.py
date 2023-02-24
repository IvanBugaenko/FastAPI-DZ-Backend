from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UsersResponse(BaseModel):
    id: int
    username: str
    password_hashed: str
    role: str
    created_at: datetime
    created_by: int
    modified_at: Optional[datetime]
    modified_by: Optional[int]

    class Config:
        orm_mode = True
    