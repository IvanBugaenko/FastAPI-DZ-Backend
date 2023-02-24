from sqlalchemy import Column, Integer, String, DateTime
from src.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.users import Users
from datetime import datetime


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'))

    created21 = relationship('Users', foreign_keys=[created_by], backref='users2.1')
    modified22 = relationship('Users', foreign_keys=[modified_by], backref='users2.2')
