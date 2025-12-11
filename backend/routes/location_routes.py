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
    "is_vegan": {"type": "boolean", "attribute": "is_vegan", "operator": "eq"},
    "is_vegetarian": {"type": "boolean", "attribute": "is_vegetarian", "operator": "eq"},
    "is_gluten_free": {"type": "boolean", "attribute": "is_gluten_free", "operator": "eq"},
    "is_dairy_free": {"type": "boolean", "attribute": "is_dairy_free", "operator": "eq"},
    "is_low_carb": {"type": "boolean", "attribute": "is_low_carb", "operator": "eq"},
    "is_nut_free": {"type": "boolean", "attribute": "is_nut_free", "operator": "eq"},
    
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
    "is_closed": {"type": "boolean", "attribute": "is_closed", "operator": "eq"},
}


bp = Blueprint('location', __name__, url_prefix='/locations')

@bp.route("/", methods=["GET"])
def get_locations():
    location_id = "c630d9ea-5545-4bf7-90bf-dfba7f8970a8"
    
    
    # Read parameters with defaults
    lat = request.args.get("lat", type=float, default=0.0)
    lng = request.args.get("lng", type=float, default=0.0)
    radius = request.args.get("range", type=float, default=DEFAULT_RANGE_KM)

    # Enforce max range
    radius = min(radius, MAX_RANGE_KM)
    
    # Default join between Location/About/Other Hours/Working Hours
    query = (
        db.session.query(Location)
        .options(
            selectinload(Location.about),
            selectinload(Location.other_hours),
            selectinload(Location.working_hours),
            selectinload(Location.items),
            
        )
    )
    
    # Geolocation filterss
    if lat is not None and lng is not None:
        distance_expr = 6371 * func.acos(
        func.cos(func.radians(lat)) *
        func.cos(func.radians(Location.latitude)) *
        func.cos(func.radians(Location.longitude) - func.radians(lng)) +
        func.sin(func.radians(lat)) *
        func.sin(func.radians(Location.latitude))
        )

        query = query.filter(distance_expr <= radius)
    
    # Filters on main table location
    query = apply_dynamic_filters(query, Location, restaurant_filters)
    
    # Filters on working hours
    if any(param in request.args for param in working_hours_filters.keys()):
        query = query.join(Location.working_hours)
        query = apply_dynamic_filters(query, Location, working_hours_filters, join_model=LocationWorkingHours)
        query = query.distinct()
        
    # --- Filters on services (other_hours) ---
    if any(param in request.args for param in services_filters.keys()):
        query = query.join(Location.about)  # assuming `other_hours` relationship points to LocationService
        query = apply_dynamic_filters(query, Location, services_filters, join_model=LocationAbout)
        query = query.distinct()
        
    # Filters on other_hours table
    has_other_hours_filter = any(
        param in request.args or (
            other_hours_filters[param]["type"] == "number" and (
                request.args.get(f"{param}_min") is not None or
                request.args.get(f"{param}_max") is not None
            )
        )
        for param in other_hours_filters
    )

    if has_other_hours_filter:
        query = query.join(Location.other_hours)  # assumes relationship points to LocationOtherHours
        query = apply_dynamic_filters(query, Location, other_hours_filters, join_model=LocationOtherHours)
        query = query.distinct()

    # Check if any menu item filter applies
    has_menu_item_filter = False
    for param in menu_item_filters.keys():
        if param in request.args:
            has_menu_item_filter = True
            break
        
        # For numeric fields, check if _min or _max is present
        if menu_item_filters[param]["type"] == "number":
            if request.args.get(f"{param}_min") is not None or request.args.get(f"{param}_max") is not None:
                has_menu_item_filter = True
                break

    if has_menu_item_filter:
        query = query.join(Location.items)
        query = apply_dynamic_filters(query, Location, menu_item_filters, join_model=Item)
        query = query.distinct()
    
    print(query)
    # if location_id:
    #     query = query.filter(Location.id == location_id)

    locations = query.all()


    output = [
        {
           
            'id':loc.id,
            'name':loc.name,
            'slug':loc.slug,
            'site':loc.site,
            'category':loc.category,
            'booking_link':loc.booking_link,
            'company_phone':loc.company_phones,
            'company_slug':loc.company_slug,
            'email':loc.email,
            'google_id':loc.google_id,
            'latitude':loc.latitude,
            'longitude':loc.longitude,
            'photo':loc.photo,
            'place_id':loc.place_id,
            'price_range':loc.price_range,
            'sub_types':loc.subtypes,
            'type':loc.type,
            'rating':loc.rating,
            'order_link':loc.order_link,
            'reservation_link':loc.reservation_link,
            'reviews_link':loc.reviews_link,
            
            
            'services': [
                {'category':item.category,'key':item.key,'value':item.value}
                for item in loc.about
            ],
            # ,'from':item.open_time,'to':item.close_time,
            'other_hours': [
                {'day':item.day_of_week,'is_closed':item.is_closed,'category':item.category,'from':time_to_str(item.open_time),'to':time_to_str(item.close_time)}
                for item in loc.other_hours
            ],
            'working_hours': [
                {'day':item.day_of_week,'is_closed':item.is_closed,'from':time_to_str(item.open_time),'to':time_to_str(item.close_time)}
                for item in loc.working_hours
            ],
            'menu_items': [
                {c.name: getattr(item, c.name) for c in Item.__table__.columns}
                for item in loc.items
            ]
        }
        for loc in locations
    ]

    options = get_options()
    
    result = {
        'rows':output,
        'options':options
    }
    return jsonify(result)

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
            

def get_options():
    
    all_filters= {}
    
    restaurant = process_category(Location,restaurant_filters)
    all_filters.update(restaurant)
    
    services = process_category(LocationAbout,services_filters)
    all_filters.update(services)
    
    menu_items = process_category(Item,menu_item_filters)
    all_filters.update(menu_items)
    return all_filters