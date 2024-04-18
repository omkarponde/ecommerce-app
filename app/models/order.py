from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base

# Define association table for the many-to-many relationship
order_product_association = Table(
    'order_product_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
    # TODO: add quantity
)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_product_association, back_populates="orders")
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)  # add server default
    updated_at = Column(DateTime)
    # TODO: status = Completed/in progress/canceled

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id})>"
