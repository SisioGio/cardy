from app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String, primary_key=True)
    slug = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    locations = db.relationship("Location", backref="company", lazy=True)
