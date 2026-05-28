from sqlalchemy.orm import Session
from app.models.db_base import Restaurant

class RestaurantService:
    def __init__(self, db: Session):
        self.db = db

    def list_restaurants(self):
        """Return all restaurants ordered by name."""
        return self.db.query(Restaurant).order_by(Restaurant.name).all()

    def get_restaurant(self, restaurant_id: int):
        """Return a single restaurant or raise 404‑style exception."""
        restaurant = self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise ValueError(f"Restaurant {restaurant_id} not found")
        return restaurant

    def add_restaurant(self, **kwargs):
        """Create a new restaurant from provided fields.
        Expected keys: name, address, google_place_url, google_map_url,
        website_url, yelp_url, visited_yn, avg_score, review_count.
        """
        restaurant = Restaurant(**kwargs)
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def update_restaurant(self, restaurant_id: int, **kwargs):
        """Update fields of an existing restaurant and return it."""
        restaurant = self.get_restaurant(restaurant_id)
        for key, value in kwargs.items():
            setattr(restaurant, key, value)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete_restaurant(self, restaurant_id: int):
        """Delete a restaurant record."""
        restaurant = self.get_restaurant(restaurant_id)
        self.db.delete(restaurant)
        self.db.commit()
        return True
