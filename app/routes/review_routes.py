import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy import func

from app.services.db_service import get_db
from app.models.db_base import Review, Restaurant, Photo
from app.schemas.review_schema import ReviewCreateSchema, ReviewResponseSchema

router = APIRouter(prefix="/reviews", tags=["reviews"], redirect_slashes=False)

@router.post("", status_code=status.HTTP_201_CREATED)
async def submit_review_form(
    restaurant_id: int = Form(...),
    reviewer_email: str = Form(...),
    score: float = Form(...),
    comments: str = Form(None),
    price_subscore: int = Form(0),
    salsa_subscore: int = Form(0),
    tortillas_subscore: int = Form(0),
    condiments_subscore: int = Form(0),
    ambiance_subscore: int = Form(0),
    flavor_subscore: int = Form(0),
    service_subscore: int = Form(0),
    homemade_tortillas_yn: bool = Form(False),
    other_notes: str = Form(None),
    photo_file_1: UploadFile = File(None),
    photo_file_2: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # verify reviewer is authorized
    reviewer = db.query(AuthorizedReviewer).filter(AuthorizedReviewer.email == reviewer_email).first()
    if not reviewer:
        raise HTTPException(status_code=403, detail="Reviewer not authorized")
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # handle photo uploads
    photo1 = None
    photo2 = None
    upload_dir = "static/uploads"
    import os, shutil, uuid
    if photo_file_1:
        filename = f"{uuid.uuid4().hex}_{photo_file_1.filename}"
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(photo_file_1.file, buffer)
        photo1 = Photo(url=f"/static/uploads/{filename}")
        db.add(photo1)
        db.flush()
    if photo_file_2:
        filename = f"{uuid.uuid4().hex}_{photo_file_2.filename}"
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(photo_file_2.file, buffer)
        photo2 = Photo(url=f"/static/uploads/{filename}")
        db.add(photo2)
        db.flush()
    db_review = Review(
        restaurant_id=restaurant_id,
        reviewer_email=reviewer_email,
        score=score,
        comments=comments,
        price_subscore=price_subscore,
        salsa_subscore=salsa_subscore,
        tortillas_subscore=tortillas_subscore,
        condiments_subscore=condiments_subscore,
        ambiance_subscore=ambiance_subscore,
        flavor_subscore=flavor_subscore,
        service_subscore=service_subscore,
        homemade_tortillas_yn=homemade_tortillas_yn,
        other_notes=other_notes,
        photo_1_id=photo1.id if photo1 else None,
        photo_2_id=photo2.id if photo2 else None,
    )
    db.add(db_review)
    db.commit()
    # recompute restaurant aggregates
    stats = db.query(func.avg(Review.score).label("avg"), func.count(Review.id).label("cnt")).filter(Review.restaurant_id == restaurant_id).one()
    db.query(Restaurant).filter(Restaurant.id == restaurant_id).update({Restaurant.avg_score: stats.avg, Restaurant.review_count: stats.cnt})
    db.commit()
    db.refresh(db_review)
    return RedirectResponse(url=f"/reviews/success/{db_review.id}", status_code=303)

@router.get("/success/{review_id}", response_class=HTMLResponse, include_in_schema=False)
async def review_success_page(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")


    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "..", "app", "templates"))
    html = templates.get_template("review_success.html").render(
        review=review,
        restaurant=review.restaurant,
        photo1=review.photo1,
        photo2=review.photo2,
        back_url="/public/list-restaurants",
    )
    return HTMLResponse(content=html)

@router.get("/restaurant/{restaurant_id}", response_model=list[ReviewResponseSchema])
async def get_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.restaurant_id == restaurant_id).all()
    return [ReviewResponseSchema.from_orm(r) for r in reviews]