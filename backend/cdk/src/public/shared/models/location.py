from app import db
from datetime import datetime
from flask import  jsonify
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.String, primary_key=True)
    slug = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    location_name = db.Column(db.String(256), nullable=True)
    menu_categories_order = db.Column(db.ARRAY(db.String))
    company_slug = db.Column(db.String, db.ForeignKey('company.slug', ondelete='CASCADE'), nullable=False)
    verified_by_user = db.Column(db.Boolean, default=False)
    verified_by_owner = db.Column(db.Boolean, default=False)
    reviews_link = db.Column(db.String(256))
    site = db.Column(db.String(256))
    subtypes = db.Column(db.ARRAY(db.String))
    category = db.Column(db.String(256))
    type = db.Column(db.String(256))
    company_phone = db.Column(db.String)
    company_phones = db.Column(db.ARRAY(db.String))
    company_facebook = db.Column(db.String)
    company_instagram = db.Column(db.String)
    email = db.Column(db.ARRAY(db.String))
    latitude = db.Column(db.Numeric(10,5))
    longitude = db.Column(db.Numeric(10,5))
    time_zone = db.Column(db.String)
    rating = db.Column(db.Numeric(5,2))
    photos_count = db.Column(db.Integer)
    photo = db.Column(db.String)
    price_range = db.Column(db.Integer)
    owner_id = db.Column(db.String)
    reservation_link = db.Column(db.String)
    booking_link = db.Column(db.String)
    order_link = db.Column(db.String)
    location_link = db.Column(db.String)
    place_id = db.Column(db.String)
    google_id = db.Column(db.String)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    menus_categories = db.relationship("MenuCategory", backref="location", lazy=True)
    menus = db.relationship("Menu", backref="location", lazy=True)
    item_categories = db.relationship("ItemCategory", backref="location", lazy=True)
    items = db.relationship("Item", backref="location", lazy=True)
    working_hours = db.relationship("LocationWorkingHours", backref="location", lazy=True)
    other_hours = db.relationship("LocationOtherHours", backref="location", lazy=True)
    about = db.relationship("LocationAbout", backref="location", lazy=True)
    tag_categories = db.relationship("TagCategory", backref="location", lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}