from .base import Base
from sqlalchemy import Column, Integer, String,TEXT,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .menu_category import MenuCategory
from .location_about import LocationAbout
from .location_other_hours import LocationOtherHours
from .location_working_hours import LocationWorkingHours
from .menu import Menu
from .item_category import ItemCategory
from .tag_category import TagCategory
class Location(Base):
    __tablename__ = 'location'
    id = Column(String, primary_key=True)
    slug = Column(String(256), unique=True, nullable=False)
    name = Column(String(256), nullable=False)
    location_name = Column(String(256), nullable=True)
    menu_categories_order = Column(ARRAY(String))
    company_slug = Column(String, ForeignKey('company.slug', ondelete='CASCADE'), nullable=False)
    verified_by_user = Column(Boolean, default=False)
    verified_by_owner = Column(Boolean, default=False)
    reviews_link = Column(String(256))
    site = Column(String(256))
    city = Column(TEXT)
    street = Column(String(256))
    country = Column(String(256))
    postal_code = Column(String(256))
    subtypes = Column(ARRAY(String))
    category = Column(String(256))
    type = Column(String(256))
    company_phone = Column(String)
    company_phones = Column(ARRAY(String))
    company_facebook = Column(String)
    company_instagram = Column(String)
    email = Column(ARRAY(String))
    latitude = Column(Numeric(10,5))
    longitude = Column(Numeric(10,5))
    time_zone = Column(String)
    rating = Column(Numeric(5,2))
    photos_count = Column(Integer)
    photo = Column(String)
    price_range = Column(Integer)
    owner_id = Column(String)
    reservation_link = Column(String)
    booking_link = Column(String)
    order_link = Column(String)
    location_link = Column(String)
    place_id = Column(String)
    google_id = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    menus_categories = relationship("MenuCategory", backref="location", lazy=True)
    menus = relationship("Menu", backref="location", lazy=True)
    item_categories = relationship("ItemCategory", backref="location", lazy=True)
    items = relationship("Item", backref="location", lazy=True)
    working_hours = relationship("LocationWorkingHours", backref="location", lazy=True)
    other_hours = relationship("LocationOtherHours", backref="location", lazy=True)
    about = relationship("LocationAbout", backref="location", lazy=True)
    tag_categories = relationship("TagCategory", backref="location", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}