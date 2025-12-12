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
