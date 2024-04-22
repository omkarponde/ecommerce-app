from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

User = Base.classes.users
Role = Base.classes.roles
# Product = Base.classes.products

