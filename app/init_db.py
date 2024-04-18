from app.db import engine, Base
from app.models import order, user, product

Base.metadata.create_all(bind=engine)
