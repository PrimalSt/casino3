# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from models import Base

# Параметр future=True рекомендуется для SQLAlchemy 2.0
engine = create_engine(config.DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    Base.metadata.create_all(bind=engine)