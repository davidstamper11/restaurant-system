import sys, os
sys.path.append(os.getcwd())
from fastapi.testclient import TestClient
from app.main import app
from app.services.db_service import get_db
from app.models.db_base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.authorized_reviewer import AuthorizedReviewer
def hash_password(pwd: str) -> str:
    import hashlib
    return hashlib.sha256(pwd.encode()).hexdigest()

# Use a temporary SQLite DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_admin.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    admin = AuthorizedReviewer(name="admin", email="admin@example.com", is_admin_yn=True, password=hash_password("secret"))
    db.add(admin)
    db.commit()
    db.close()

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

client = TestClient(app)

def test_admin_login_success():
    response = client.post("/admin/login", data={"email": "admin@example.com", "password": "secret"})
    assert response.status_code == 302
    assert "admin_session" in response.cookies

def test_admin_login_failure():
    response = client.post("/admin/login", data={"email": "admin@example.com", "password": "wrong"})
    assert response.status_code == 403
