from app import db
from datetime import datetime

class MenuCategory(db.Model):
    __tablename__ = 'menu_category'
    __table_args__ = (
        db.UniqueConstraint('name', 'location_id', name='uq_menu_category_name_location'),
    )
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    menus_order = db.Column(db.ARRAY(db.String))
    location_id = db.Column(db.String, db.ForeignKey('location.id', ondelete='CASCADE'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    menus = db.relationship("Menu", backref="menu_category", lazy=True)
