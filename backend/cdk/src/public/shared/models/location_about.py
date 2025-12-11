from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
class LocationAbout(Base):
    __tablename__ = 'location_about'
    id = Column(String, primary_key=True)
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'))
    category = Column(String)
    key = Column(String)
    value = Column(Boolean)
    