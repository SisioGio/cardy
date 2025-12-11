
import os
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker,joinedload,selectinload
from dotenv import load_dotenv
import os
from shared.models.item import Item
from shared.models.location import Location
from shared.models.location_about import LocationAbout
from shared.models.location_other_hours import LocationOtherHours
from shared.models.location_working_hours import LocationWorkingHours
from decimal import Decimal


from utils import get_secret
import json


load_dotenv()


DB_SECRET_CRED_NAME = os.getenv("RDS_SECRET_NAME")
DB_CREDENTIALS = get_secret(DB_SECRET_CRED_NAME)
DB_ENDPOINT=os.getenv("DB_ENDPOINT")
DB_DATABASE = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f'postgresql+pg8000://{DB_CREDENTIALS['username']}:{DB_CREDENTIALS['password']}@{DB_ENDPOINT}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


DEFAULT_RANGE_KM = 2
MAX_RANGE_KM = 50




def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    
    lat = float(params.get("lat",48.08622))
    lng = float(params.get("lng", 11.54037))
    radius = min(float(params.get("range", DEFAULT_RANGE_KM)), MAX_RANGE_KM)
    print(f"Fetching for {lat},{lng} (radius: {radius})")
    session = SessionLocal()
    

    city = params.get("city",None)


    # Base query with joinedload relationships
    query = (
        session.query(Location)
        .options(
            selectinload(Location.about),
            selectinload(Location.other_hours),
            selectinload(Location.working_hours),
            selectinload(Location.items),
            
        )
    )
    
    # Filter by city if provided
    if city:
        query = query.filter(Location.city.ilike(f"%{city.strip()}%"))

    # Filter by coordinates if provided and valid
    if lat is not None and lng is not None:
        distance_expr = 6371 * func.acos(
            func.cos(func.radians(lat)) *
            func.cos(func.radians(Location.latitude)) *
            func.cos(func.radians(Location.longitude) - func.radians(lng)) +
            func.sin(func.radians(lat)) *
            func.sin(func.radians(Location.latitude))
        )
        query = query.filter(distance_expr <= radius)

    # --- Restaurant filters ---
    restaurant_filters = {
        'rest_name': lambda v: Location.name.ilike(f"%{v}%"),
        'rest_rating': lambda v: Location.rating >= float(v),
        'rest_price_range': lambda v: Location.price_range == int(v),
        'rest_type': lambda v: Location.type.ilike(f"%{v}%"),
        'rest_sub_type': lambda v: Location.subtypes.ilike(f"%{v}%")
    }
    for key, f in restaurant_filters.items():
        if key in params:
            query = query.filter(f(params[key]))

    # --- Working hours filters ---
    working_hours_filters = {
        "wh_day": lambda v: LocationWorkingHours.day_of_week == v,
        "wh_open_after": lambda v: LocationWorkingHours.open_time >= v,
        "wh_open_before": lambda v: LocationWorkingHours.open_time <= v,
        "wh_close_after": lambda v: LocationWorkingHours.close_time >= v,
        "wh_close_before": lambda v: LocationWorkingHours.close_time <= v,
        "wh_is_closed": lambda v: LocationWorkingHours.is_closed == (v.lower() == 'true')
    }
    if any(k in params for k in working_hours_filters.keys()):
        query = query.join(Location.working_hours)
        for key, f in working_hours_filters.items():
            if key in params:
                query = query.filter(f(params[key]))

    # --- Services filters ---
    services_filters = {
        "service_category": lambda v: LocationAbout.category == v,
        "service_key": lambda v: LocationAbout.key == v,
        "service_value": lambda v: LocationAbout.value == (v.lower() == 'true')
    }
    if any(k in params for k in services_filters.keys()):
        query = query.join(Location.about)
        for key, f in services_filters.items():
            if key in params:
                query = query.filter(f(params[key]))

    # --- Other hours filters ---
    other_hours_filters = {
        "category": lambda v: LocationOtherHours.category.ilike(f"%{v}%"),
        "day": lambda v: LocationOtherHours.day_of_week.ilike(f"%{v}%"),
        "from": lambda v: LocationOtherHours.open_time == v,
        "to": lambda v: LocationOtherHours.close_time == v,
        "is_closed": lambda v: LocationOtherHours.is_closed == (v.lower() == 'true')
    }
    if any(k in params for k in other_hours_filters.keys()):
        query = query.join(Location.other_hours)
        for key, f in other_hours_filters.items():
            if key in params:
                query = query.filter(f(params[key]))

    # --- Menu items filters ---
    menu_item_filters = {
        "item_name": lambda v: Item.name.ilike(f"%{v}%"),
        "cuisine_type": lambda v: Item.cuisine_type.ilike(f"%{v}%"),
        "price_min": lambda v: Item.price >= float(v),
        "price_max": lambda v: Item.price <= float(v),
        "is_vegan": lambda v: Item.is_vegan == (v.lower() == 'true'),
        "is_vegetarian": lambda v: Item.is_vegetarian == (v.lower() == 'true'),
    }
    if any(k in params for k in menu_item_filters.keys()):
        query = query.join(Location.items)
        for key, f in menu_item_filters.items():
            if key in params:
                query = query.filter(f(params[key]))

    query = query.distinct()
    
    
    locations = query.all()

    # --- Build JSON ---
    def time_to_str(t):
        return t.strftime("%H:%M") if t else None

    output = []
    for loc in locations:
        output.append({
            'id': loc.id,
            'name': loc.name,
            'slug': loc.slug,
            'site': loc.site,
            'category': loc.category,
            'booking_link': loc.booking_link,
            'company_phone': loc.company_phones,
            'company_slug': loc.company_slug,
            'email': loc.email,
            'google_id': loc.google_id,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'photo': loc.photo,
            'place_id': loc.place_id,
            'price_range': loc.price_range,
            'sub_types': loc.subtypes,
            'type': loc.type,
            'rating': loc.rating,
            'order_link': loc.order_link,
            'reservation_link': loc.reservation_link,
            'reviews_link': loc.reviews_link,
            'services': [
                {'category': s.category, 'key': s.key, 'value': s.value}
                for s in loc.about
            ],
            'other_hours': [
                {'day': o.day_of_week, 'is_closed': o.is_closed,
                 'category': o.category, 'from': time_to_str(o.open_time),
                 'to': time_to_str(o.close_time)}
                for o in loc.other_hours
            ],
            'working_hours': [
                {'day': w.day_of_week, 'is_closed': w.is_closed,
                 'from': time_to_str(w.open_time), 'to': time_to_str(w.close_time)}
                for w in loc.working_hours
            ],
            'menu_items': [
                {c.name: getattr(item, c.name) for c in Item.__table__.columns}
                for item in loc.items
            ]
        })

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({'rows': convert_decimals(output), 'options': {},'counter':len(output)})
    }


def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj