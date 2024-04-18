from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models import order_product_association
from app.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="products")
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    # TODO: quantity available

    orders = relationship("Order", secondary=order_product_association, back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, user_id={self.user_id}, name='{self.name}', price={self.price}, created_at={self.created_at})>"
