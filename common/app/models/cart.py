from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Cart(Base):
    __tablename__ = 'carts'
    __table_args__ = {'schema': 'cart_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user_schema.users.id'), nullable=False)
    user = relationship("User", back_populates="cart")

    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'
    __table_args__ = {'schema': 'cart_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart_schema.carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product_schema.products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
