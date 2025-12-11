from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class ItemCategory(Base):
    __tablename__ = 'item_category'
    __table_args__ = (
        UniqueConstraint('name', 'location_id','menu_id', name='uq_item_name_loc_menu'),
    )
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    items_order = Column(ARRAY(String))
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    menu_id = Column(String, ForeignKey('menu.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("Item", backref="item_category", lazy=True)
