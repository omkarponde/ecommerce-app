from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare an Automap Base
Base = automap_base()
Base.prepare(engine, reflect=True, schema="product_schema")
