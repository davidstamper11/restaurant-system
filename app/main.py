import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import public_routes, review_routes, admin_routes

app.add_middleware(admin_routes.AdminAuthMiddleware)

# Upload directory – works locally and on Render
UPLOAD_DIR = os.getenv("UPLOAD_DIR") or os.path.join(os.getcwd(), "tmp", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve uploaded images at /static/uploads/<filename>
app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Serve other static assets (css, js, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(review_routes.router)
app.include_router(admin_routes.router)