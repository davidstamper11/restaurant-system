from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    google_place_url = Column(String, nullable=True)
    google_map_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    yelp_url = Column(String, nullable=True)
    visited_yn = Column(Boolean, default=False)
    avg_score = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    reviews = relationship('Review', back_populates='restaurant')

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    reviewer_email = Column(String)
    score = Column(Float)  # 0.0 to 5.0
    comments = Column(Text, nullable=True)
    price_subscore = Column(Integer)
    salsa_subscore = Column(Integer)
    tortillas_subscore = Column(Integer)
    condiments_subscore = Column(Integer)
    ambiance_subscore = Column(Integer)
    flavor_subscore = Column(Integer)
    service_subscore = Column(Integer)
    homemade_tortillas_yn = Column(Boolean, default=False)
    photo_1_id = Column(Integer, ForeignKey('photos.id'), nullable=True)
    photo_2_id = Column(Integer, ForeignKey('photos.id'), nullable=True)
    other_notes = Column(Text, nullable=True)
    restaurant = relationship('Restaurant', back_populates='reviews')
    photo1 = relationship('Photo', foreign_keys=[photo_1_id])
    photo2 = relationship('Photo', foreign_keys=[photo_2_id])


class AuthorizedReviewer(Base):
    __tablename__ = 'reviewers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    is_admin_yn = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('reviewers.id'), nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    deleted_by = Column(Integer, ForeignKey('reviewers.id'), nullable=True)
    password = Column(String, nullable=True)