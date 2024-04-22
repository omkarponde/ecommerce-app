from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'payment_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order_schema.orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default='pending', nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_method = Column(String, default='COD', nullable=False)

    order = relationship("Order")  #, schema="order_schema")
