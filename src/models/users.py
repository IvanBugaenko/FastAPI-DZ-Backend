from sqlalchemy import Column, Integer, String, DateTime
from src.models.base import Base
from sqlalchemy import ForeignKey
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password_hashed = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'))
