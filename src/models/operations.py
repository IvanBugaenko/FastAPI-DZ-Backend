from sqlalchemy import Column, Integer, Float, DateTime
from src.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.tanks import Tanks
from src.models.products import Products
from src.models.users import Users
from datetime import datetime


class Operations(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float, nullable=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    tank_id = Column(Integer, ForeignKey('tanks.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'))

    tank = relationship('Tanks', foreign_keys=[tank_id], backref='tanks')
    
    product1 = relationship('Products', foreign_keys=[product_id], backref='products1')
    created11 = relationship('Users', foreign_keys=[created_by], backref='users1.1')
    modified12 = relationship('Users', foreign_keys=[modified_by], backref='users1.2')
