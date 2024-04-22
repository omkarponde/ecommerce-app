from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'user_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Define the one-to-many relationship with users
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'user_schema'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)
    role_id = Column(Integer, ForeignKey('user_schema.roles.id'))
    role = relationship("Role", back_populates="users")

    # Define one-to-many relationship with orders
    orders = relationship("Order", back_populates="user")

    # Define one-to-many relationship with products
    products = relationship("Product", back_populates="user")

    cart = relationship("Cart", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


