import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import public_routes, review_routes, admin_routes

app = FastAPI(title="Restaurant Review System")

# ----------------------------------------------------------------------
# ONE‑TIME STARTUP: Hash plain‑text passwords for admin accounts
# ----------------------------------------------------------------------
from app.models.authorized_reviewer import AuthorizedReviewer
from app.services.db_service import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@app.on_event("startup")
def rehash_admin_passwords():
    db = next(get_db())
    admins = db.query(AuthorizedReviewer).filter(AuthorizedReviewer.is_admin_yn == True).all()
    for admin in admins:
        if admin.password and not admin.password.startswith("$pbkdf2-sha256$"):
            # set a known temporary password
            admin.password = pwd_context.hash("TempPass123")
    db.commit()

app.add_middleware(admin_routes.AdminAuthMiddleware)
# ensure the uploads directory exists on startup (Render provides a writable /tmp)
os.makedirs("/tmp/uploads", exist_ok=True)

# mount upload path BEFORE general static
app.mount("/static/uploads", StaticFiles(directory="/tmp/uploads"), name="uploads")

# static assets (css, js, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(review_routes.router)
app.include_router(admin_routes.router)