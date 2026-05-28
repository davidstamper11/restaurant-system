from pydantic import BaseModel, HttpUrl, validator
from typing import Optional
class RestaurantBaseSchema(BaseModel):
    name: str
    address: str
    google_place_url: Optional[HttpUrl] = None
    google_map_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None
    yelp_url: Optional[HttpUrl] = None
    visited_yn: bool = False
class RestaurantCreateSchema(RestaurantBaseSchema):
    """Fields required when *creating* a restaurant."""
    pass
class RestaurantUpdateSchema(RestaurantBaseSchema):
    """All fields are optional when *updating*."""
    name: Optional[str] = None
    address: Optional[str] = None
    @validator("*", pre=True, always=True)
    def empty_strings_to_none(cls, v):
        # Convert blank strings to None so SQLAlchemy stores NULL instead of "".
        return v if v != "" else None