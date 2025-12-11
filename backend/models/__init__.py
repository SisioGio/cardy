from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all model classes AFTER db is created
from .company import Company
from .location import Location
from .location_working_hours import LocationWorkingHours
from .location_other_hours import LocationOtherHours
from .location_about import LocationAbout
from .menu import Menu
from .menu_category import MenuCategory
from .item_category import ItemCategory
from .tag_category import TagCategory
from .tag import Tag
from .item import Item
from .ingredients import Ingredients
from .allergens import Allergens

__all__ = [
    "db",
    "Company",
    "Location",
    "LocationWorkingHours",
    "LocationOtherHours",
    "LocationAbout",
    "Menu",
    "MenuCategory",
    "ItemCategory",
    "TagCategory",
    "Tag",
    "Item",
    "Ingredients",
    "Allergens",
]
