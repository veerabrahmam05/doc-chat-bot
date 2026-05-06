from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.env import settings
from src.models.schemas import Base

DATABASE_URL = settings.database_url

engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()