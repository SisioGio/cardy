
from datetime import datetime
from .base import Base
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = 'company'
    id =Column(String, primary_key=True)
    slug = Column(String(256), unique=True, nullable=False)
    name = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    locations = relationship("Location", backref="company", lazy=True)
