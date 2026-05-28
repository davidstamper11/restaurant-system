from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure model classes are imported so they register with Base
from . import db_base  # noqa: F401
from .db_base import Base
from ..config import DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def init_db():
    """Create all tables defined in the models."""
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)