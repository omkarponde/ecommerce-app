from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models import order_product_association
from app.db import Base
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'product_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_schema.users.id'), nullable=False)
    user = relationship("User", back_populates="products")
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    orders = relationship("Order", secondary=order_product_association, back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, user_id={self.user_id}, name='{self.name}', price={self.price}, created_at={self.created_at})>"
