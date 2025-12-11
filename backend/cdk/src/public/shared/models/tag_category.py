from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .tag import Tag
class TagCategory(Base):
    __tablename__ = 'tag_category'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tags = relationship("Tag", backref="tag_category", lazy=True)
