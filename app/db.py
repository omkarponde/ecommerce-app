from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
