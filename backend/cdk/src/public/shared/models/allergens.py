from .base import Base
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship
class Allergens(Base):
    __tablename__ = 'allergens'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    item_id = Column(String, ForeignKey('item.id', ondelete='CASCADE'))
