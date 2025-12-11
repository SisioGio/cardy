from app import db
from datetime import datetime

class ItemCategory(db.Model):
    __tablename__ = 'item_category'
    __table_args__ = (
        db.UniqueConstraint('name', 'location_id','menu_id', name='uq_item_name_loc_menu'),
    )
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    items_order = db.Column(db.ARRAY(db.String))
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    menu_id = db.Column(db.String, db.ForeignKey('menu.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship("Item", backref="item_category", lazy=True)
