from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UsersRequest(BaseModel):
    username: Optional[str]
    password_text: Optional[str]
    role: Optional[str]
