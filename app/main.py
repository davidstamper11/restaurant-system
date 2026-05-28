from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import public_routes, review_routes, admin_routes

app = FastAPI(title="Restaurant Review System")
app.mount("/static", StaticFiles(directory="static"), name="static")
# Serve uploaded photos
app.mount("/static/uploads", StaticFiles(directory="/tmp/uploads"), name="uploads")
app.include_router(public_routes.router)
app.include_router(review_routes.router)
app.include_router(admin_routes.router)
