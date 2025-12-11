from app import db
from datetime import datetime

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tag_category_id = db.Column(db.String, db.ForeignKey('tag_category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
