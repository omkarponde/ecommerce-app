from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True, schema="order_schema")
Base.prepare(engine, reflect=True, schema="public")
Base.prepare(engine, reflect=True, schema="product_schema")