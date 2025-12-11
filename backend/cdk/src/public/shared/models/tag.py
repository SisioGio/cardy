from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    tag_category_id = Column(String, ForeignKey('tag_category.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
