from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

print("Here")
Order = Base.classes.orders
OrderProductAssociation = Base.classes.order_product_associations
Product = Base.classes.products
