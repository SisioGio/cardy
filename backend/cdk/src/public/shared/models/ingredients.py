from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
class Ingredients(Base):
    __tablename__ = 'ingredients'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Numeric(10,2))
    item_id = Column(String, ForeignKey('item.id', ondelete='CASCADE'))
