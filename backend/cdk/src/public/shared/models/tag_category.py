from app import db
from datetime import datetime

class TagCategory(db.Model):
    __tablename__ = 'tag_category'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tags = db.relationship("Tag", backref="tag_category", lazy=True)
