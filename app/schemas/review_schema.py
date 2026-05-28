from pydantic import BaseModel, HttpUrl, EmailStr, Field

class ReviewCreateSchema(BaseModel):
    restaurant_id: int
    reviewer_email: EmailStr
    score: int = Field(..., ge=0, le=5)
    comments: str | None = None

class ReviewResponseSchema(BaseModel):
    id: int
    restaurant_id: int
    reviewer_email: EmailStr
    score: int
    comments: str | None
    created_at: str

    class Config:
        orm_mode = True
