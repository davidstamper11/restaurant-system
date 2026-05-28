import os
from sqlalchemy import create_engine
from .db_base import Base
# SQLite DB path (relative to project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
def init_db() -> None:
    """Create all tables (or update when run)."""
    Base.metadata.create_all(engine)
if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")