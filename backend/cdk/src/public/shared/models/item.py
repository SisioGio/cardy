from .base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String,DateTime,UniqueConstraint,Text,Boolean,Numeric,ForeignKey,ARRAY,JSON
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = (
        UniqueConstraint('name', 'location_id', 'menu_id', name='uq_item_cat_name_loc_menu'),
    )
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    short_description = Column(Text)
    full_description = Column(Text)
    price = Column(Numeric(10,2))
    currency = Column(String)
    portion_size = Column(String)
    cuisine_type = Column(String)
    preparation_method = Column(String)
    is_vegan = Column(Boolean, default=False)
    is_vegetarian = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_dairy_free = Column(Boolean, default=False)
    is_nut_free = Column(Boolean, default=False)
    is_low_carb = Column(Boolean, default=False)
    spiciness_level = Column(String)
    special_notes = Column(Text)
    calories = Column(Numeric(10,2))
    proteins = Column(Numeric(10,2))
    carbs = Column(Numeric(10,2))
    fat = Column(Numeric(10,2))
    fiber = Column(Numeric(10,2))
    sugar = Column(Numeric(10,2))
    sodium = Column(Numeric(10,2))
    image = Column(String)
    item_category_id = Column(String, ForeignKey('item_category.id'))
    menu_id = Column(String, ForeignKey('menu.id'))
    location_id = Column(String, ForeignKey('location.id', ondelete='CASCADE'))
    option_groups_order = Column(ARRAY(String))
    is_active = Column(Boolean, default=True)
    pos_id = Column(Integer)
    background_information = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ingredients = relationship("Ingredients", backref="item", lazy=True)
    allergens = relationship("Allergens", backref="item", lazy=True)
