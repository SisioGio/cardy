from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .menu import Menu
class MenuCategory(Base):
    __tablename__ = 'menu_category'
    __table_args__ = (
        UniqueConstraint('name', 'location_id', name='uq_menu_category_name_location'),
    )
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    menus_order = Column(ARRAY(String))
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    menus = relationship("Menu", backref="menu_category", lazy=True)
