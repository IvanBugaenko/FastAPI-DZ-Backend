from sqlalchemy import Column, Integer, String, Float, DateTime
from src.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.products import Products
from src.models.users import Users
from datetime import datetime


class Tanks(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    max_capacity = Column(Float, nullable=False)
    current_capacity = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'))

    product2 = relationship('Products', backref='products2')
    created31 = relationship('Users', foreign_keys=[created_by], backref='users3.1')
    modified32 = relationship('Users', foreign_keys=[modified_by], backref='users3.2')
