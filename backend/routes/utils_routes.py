from flask import Blueprint, jsonify, request
from models import db
from models import LocationAbout
from models import LocationOtherHours
from models import LocationWorkingHours
from models import Location
from models import Company
from models import Item
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from utils.utils import *
from sqlalchemy import distinct

MAX_RANGE_KM = 50  
DEFAULT_RANGE_KM = 10 


# def time_to_str(t):
#     return t.strftime("%H:%M") if t else None


restaurant_filters = {
    'rest_name': {
        'type': 'string',
        'attribute': 'name',
        'operator': 'contains'  # default for strings
    },
    'rest_rating': {
        'type': 'number',
        'attribute': 'rating',
        'operator': 'gte'  # minimum rating
    },
    'rest_price_range': {
        'type': 'number',
        'attribute': 'price_range',
        'operator': 'eq'
    },
    'rest_sub_type': {
        'type': 'string',
        'attribute': 'subtypes',
        'operator': 'contains'
    },
    'rest_type': {
        'type': 'string',
        'attribute': 'type',
        'operator': 'contains'
    }
    
    
}
working_hours_filters = {
    "wh_day": {
        "type": "string",
        "attribute": "day_of_week",
        "operator": "eq"
    },
    "wh_open_after": {
        "type": "time",
        "attribute": "open_time",
        "operator": "gte"
    },
    "wh_open_before": {
        "type": "time",
        "attribute": "open_time",
        "operator": "lte"
    },
    "wh_close_after": {
        "type": "time",
        "attribute": "close_time",
        "operator": "gte"
    },
    "wh_close_before": {
        "type": "time",
        "attribute": "close_time",
        "operator": "lte"
    },
    "wh_is_closed": {
        "type": "bool",
        "attribute": "is_closed",
        "operator": "eq"
    },
}

services_filters = {
    "service_category": {"type": "string", "attribute": "category", "operator": "eq"},
    "service_key": {"type": "string", "attribute": "key", "operator": "eq"},
    "service_value": {"type": "bool", "attribute": "value", "operator": "eq"},
}

menu_item_filters = {
    "item_name": {"type": "string", "attribute": "name", "operator": "ilike"},
    "cuisine_type": {"type": "string", "attribute": "cuisine_type", "operator": "ilike"},
    "portion_size": {"type": "string", "attribute": "portion_size", "operator": "ilike"},
    "preparation_method": {"type": "string", "attribute": "preparation_method", "operator": "ilike"},
    "spiciness_level": {"type": "string", "attribute": "spiciness_level", "operator": "ilike"},
    "is_vegan": {"type": "bool", "attribute": "is_vegan", "operator": "eq"},
    "is_vegetarian": {"type": "bool", "attribute": "is_vegetarian", "operator": "eq"},
    "is_gluten_free": {"type": "bool", "attribute": "is_gluten_free", "operator": "eq"},
    "is_dairy_free": {"type": "bool", "attribute": "is_dairy_free", "operator": "eq"},
    "is_low_carb": {"type": "bool", "attribute": "is_low_carb", "operator": "eq"},
    "is_nut_free": {"type": "bool", "attribute": "is_nut_free", "operator": "eq"},
    
    "price_min": {"type": "number", "attribute": "price", "operator": "range"},
    "price_max": {"type": "number", "attribute": "price", "operator": "range"},
    "calories": {"type": "number", "attribute": "calories", "operator": "range"},
    "carbs": {"type": "number", "attribute": "carbs", "operator": "range"},
    "proteins": {"type": "number", "attribute": "proteins", "operator": "range"},
    "fat": {"type": "number", "attribute": "fat", "operator": "range"},
    "fiber": {"type": "number", "attribute": "fiber", "operator": "range"},
    "sugar": {"type": "number", "attribute": "sugar", "operator": "range"},
    "sodium": {"type": "number", "attribute": "sodium", "operator": "range"},
    
}

other_hours_filters = {
    "category": {"type": "string", "attribute": "category", "operator": "ilike"},
    "day": {"type": "string", "attribute": "day_of_week", "operator": "ilike"},
    "from": {"type": "string", "attribute": "open_time", "operator": "eq"}, 
    "to": {"type": "string", "attribute": "close_time", "operator": "eq"},
    "is_closed": {"type": "bool", "attribute": "is_closed", "operator": "eq"},
}


bp = Blueprint('utils', __name__, url_prefix='/utils')


def process_category(table,fields):
    
    table_options = {}
    
    for key,object  in fields.items():
        print(object)
        column = getattr(table, object['attribute'])
        if object['type'] == 'string':
            rows = db.session.query(distinct(column)).order_by(column).all()
            
            if len(rows) > 500:
                table_options[key] = {
                                    'options':[],
                                    'min':None,
                                    'max':None
                }
            else:
                
                values = []
                for row in rows:
                    v = row[0]
                    if isinstance(v, (list, tuple)):       # array column
                        values.extend(v)                   # flatten
                    else:
                        values.append(v)

                # remove duplicates + sort
                values = sorted(set(values))
                table_options[key] = {
                                        'options':values,
                                        'min':None,
                                        'max':None
                                    }
        elif object['type'] == 'time':
            
            continue
        elif object['type'] == 'number':
            max_value=  db.session.query(func.max(column)).scalar()
            min_value=db.session.query(func.min(column)).scalar()
            table_options[key] = {
                                    'options':[],
                                    'min':min_value,
                                    'max':max_value
                                }
        # elif object['type'] == 'bool':
        #     table_options[key] = {
        #                             'options':[True,False],
        #                             'min':None,
        #                             'max':None
        #                         }
    return table_options
            
@bp.route("/options", methods=["GET"])
def get_options():
    
    all_filters= {}
    
    restaurant = process_category(Location,restaurant_filters)
    all_filters.update(restaurant)
    
    services = process_category(LocationAbout,services_filters)
    all_filters.update(services)
    
    menu_items = process_category(Item,menu_item_filters)
    all_filters.update(menu_items)
    return jsonify(all_filters)

