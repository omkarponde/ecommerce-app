from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class OrderProductAssociation(Base):
    __tablename__ = 'order_product_associations'

    order_id = Column(Integer, ForeignKey('order_schema.orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product_schema.products.id'), primary_key=True)
    quantity = Column(Integer, default=1)

    # Define relationship to Order and Product
    order = relationship("Order", back_populates="products")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<OrderProductAssociation(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'order_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_schema.users.id'), nullable=False)
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary='order_product_associations', back_populates="orders")
    price = Column(Integer, nullable=False)
    status = Column(String(50), default="Processing")  # Add the status column with default value "Processing"
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)  # add server default
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status})>"
