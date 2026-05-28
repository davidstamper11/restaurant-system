from pydantic import BaseModel
class AuthorizedReviewerResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    is_admin_yn: bool
    class Config:
        from_attributes = True