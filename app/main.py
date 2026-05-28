import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import public_routes, review_routes, admin_routes

app = FastAPI(title="Restaurant Review System")

# ensure the uploads directory exists on startup (Render provides a writable /tmp)
os.makedirs("/tmp/uploads", exist_ok=True)

# static assets
app.mount("/static", StaticFiles(directory="static"), name="static")
# serve uploaded photos
app.mount("/static/uploads", StaticFiles(directory="/tmp/uploads"), name="uploads")

app.include_router(public_routes.router)
app.include_router(review_routes.router)
app.include_router(admin_routes.router)
