from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

User = Base.classes.users
Order = Base.classes.orders
Product = Base.classes.products

# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(100), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)
#     # Create master table, table name role - columns = id, name
#     role = Column(String(50), nullable=False)  # role_id - fk to role table
#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime)
#
#     # Define one-to-many relationship with orders
#     orders = relationship("Order", back_populates="user")
#
#     # Define one-to-many relationship with products
#     products = relationship("Product", back_populates="user")
#
#     def __repr__(self):
#         return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
#

