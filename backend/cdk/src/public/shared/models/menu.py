from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class Menu(Base):
    __tablename__ = 'menu'
    __table_args__ = (
        UniqueConstraint('name', 'location_id','menu_category_id', name='uq_menu_name_location_cat'),
    )
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    menu_category_id = Column(String, ForeignKey('menu_category.id'))
    item_and_item_categories_order = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    pos_id = Column(Integer)
    verified_by_user = Column(Boolean, default=False)
    verified_by_owner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("Item", backref="menu", lazy=True)
    item_categories = relationship("ItemCategory", backref="menu", lazy=True)
