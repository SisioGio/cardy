from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Time
class LocationWorkingHours(Base):
    __tablename__ = 'location_working_hours'
    id = Column(String, primary_key=True)
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'))
    day_of_week = Column(String)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_closed = Column(Boolean, default=False)
