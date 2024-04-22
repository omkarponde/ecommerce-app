from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class Shipment(Base):
    __tablename__ = 'shipments'
    __table_args__ = {'schema': 'shipment_schema'}

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order_schema.orders.id'), nullable=False)
    shipping_address = Column(String, nullable=False)
    shipping_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    tracking_number = Column(String, nullable=True, default=None)
    shipment_status = Column(String, nullable=False, default='Pending')

    order = relationship("Order")#, schema="order_schema")
