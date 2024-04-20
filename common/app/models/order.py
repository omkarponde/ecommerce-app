from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base

# Define association table for the many-to-many relationship with quantity
order_product_association = Table(
    'order_product_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('order_schema.orders.id')),
    Column('product_id', Integer, ForeignKey('product_schema.products.id')),
    Column('quantity', Integer, default=1),  # Add the quantity column with default value 1
)


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'order_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_schema.users.id'), nullable=False)
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_product_association, back_populates="orders")
    price = Column(Integer, nullable=False)
    status = Column(String(50), default="Processing")  # Add the status column with default value "Processing"
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)  # add server default
    updated_at = Column(DateTime)


    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status})>"
