from app import db
from datetime import datetime

class Menu(db.Model):
    __tablename__ = 'menu'
    __table_args__ = (
        db.UniqueConstraint('name', 'location_id','menu_category_id', name='uq_menu_name_location_cat'),
    )
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    menu_category_id = db.Column(db.String, db.ForeignKey('menu_category.id'))
    item_and_item_categories_order = db.Column(db.ARRAY(db.String))
    is_active = db.Column(db.Boolean, default=True)
    pos_id = db.Column(db.Integer)
    verified_by_user = db.Column(db.Boolean, default=False)
    verified_by_owner = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship("Item", backref="menu", lazy=True)
    item_categories = db.relationship("ItemCategory", backref="menu", lazy=True)
