import os
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.db_base import Restaurant, Review
from app.services.db_service import get_db

jinja_templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "..", "..", "app", "templates")
)
router = APIRouter(prefix="/public", tags=["public"])

@router.get("/review_form")
async def review_form(request: Request, restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    from fastapi.responses import HTMLResponse
    template = jinja_templates.get_template("review_form.html")
    html = template.render(request=request, restaurant_id=restaurant_id,
                          restaurant_name=restaurant.name if restaurant else "",
                          restaurant_address=restaurant.address if restaurant else "")
    return HTMLResponse(content=html)

@router.get("/list-restaurants")
async def list_restaurants(request: Request, db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).order_by(Restaurant.name).all()
    from fastapi.responses import HTMLResponse
    template = jinja_templates.get_template("list_restaurants.html")
    html = template.render(request=request, restaurants=restaurants)
    return HTMLResponse(content=html)

@router.get("/reviews/{restaurant_id}")
async def reviews_list(request: Request, restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    from fastapi.responses import HTMLResponse
    template = jinja_templates.get_template("reviews_list.html")
    html = template.render(request=request, restaurant=restaurant, reviews=reviews)
    return HTMLResponse(content=html)
