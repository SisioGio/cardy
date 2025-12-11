import json
import pandas as pd
import psycopg2
from slugify import slugify
import uuid
from decimal import Decimal
import re
# --------------------------
# Database connection
# --------------------------
conn = psycopg2.connect(
    host="cardy-dev.cb60yy2s4a4i.eu-central-1.rds.amazonaws.com",
    dbname="postgres",
    user="postgres",
    password="Jkd>4ou]8~([[GUcvdGut):*>WFk"
)
cur = conn.cursor()

file_path = r'C:\Users\Alessio\Projects\cardy\backend\dataflow\static\output_29112025.json'

with open(file_path,'rb') as f:
    restaurants=json.load(f)

def to_decimal(val):
    try:
        return Decimal(val) if val not in (None, "", []) else None
    except:
        return None

def parse_price_and_currency(value):
    """
    Extract numeric price and currency symbol/code.
    Returns (Decimal or None, currency string or None).
    """
    if not value or value.strip() == "":
        return None, None

    original = value.strip()

    # Regex to capture number and currency separately
    match = re.match(r"^\s*([0-9.,]+)\s*([^\d\s]+)?\s*$", original)
    if match:
        num_part = match.group(1)          # "12" or "12,50"
        currency = match.group(2) or None  # "€" or "EUR" or None
    else:
        return None, None

    # Normalize number: convert comma to dot
    num_part = num_part.replace(",", ".")

    try:
        price = Decimal(num_part)
    except:
        price = None

    return price, currency

def to_bool(value):
    """
    Safely convert common truthy/falsey values to boolean.
    Empty string, None → False.
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return value

    str_val = str(value).strip().lower()
    if str_val in ["true", "1", "yes", "y"]:
        return True
    if str_val in ["false", "0", "no", "n", ""]:
        return False

    # fallback — if unexpected, treat as False
    return False

flat_menu_items = []

for restaurant in restaurants:
    
    restaurant_site = restaurant['site']
    restaurant_name=restaurant['name']
    print(f"Processing {restaurant_name}")
    
    
    
    location_id = restaurant['id']
    menu=restaurant['menu'] or []
    
    # Create menu category for restaurant
    print('Create menu category')
    cur.execute("""
    INSERT INTO menu_category (id, name, location_id, is_active)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (name, location_id) DO UPDATE SET id = menu_category.id
    RETURNING id
    """, (str(uuid.uuid4()), 'default', location_id, True))

    menu_category_id = cur.fetchone()[0]
    # Create menu for restaurant
    cur.execute("""
    INSERT INTO menu (id, name, location_id, menu_category_id,is_active)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (name, location_id,menu_category_id)  DO UPDATE SET id = menu.id
    RETURNING id
    """, (str(uuid.uuid4()), 'default', location_id, menu_category_id,True))

    menu_id = cur.fetchone()[0]
    
    for item in menu:
        if not isinstance(item, dict):
            continue
        item_category = item.get('meal_category','default')
        item_category=item_category.strip()
        # Create category in db or get its id
        cur.execute("""
        INSERT INTO item_category (id, name, location_id, menu_id,is_active)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (name, location_id,menu_id)  DO UPDATE SET id = item_category.id
        RETURNING id
        """, (str(uuid.uuid4()), item_category, location_id,menu_id,True))
        item_category_id = cur.fetchone()[0]
        item_data=item
        
        price,currency = parse_price_and_currency(item_data.get('price'))
        insert_row = (
            str(uuid.uuid4()),                                   # id
            item_data['name'],                                   # name
            item_data.get('short_description'),                  # shortDescription
            item_data.get('full_description'),                   # fullDescription
            price,                                               # price
            currency,                                            # currency
            item_data.get('portion_size'),                       # portionSize
            item_data.get('cuisine_type'),                       # cuisineType
            item_data.get('preparation_method'),                 # preparationMethod
            to_bool(item_data.get('is_vegan', False)),                    # isVegan
            to_bool(item_data.get('is_vegetarian', False)),               # isVegetarian
            to_bool(item_data.get('is_gluten_free', False)),              # isGlutenFree
            to_bool(item_data.get('is_dairy_free', False)),               # isDairyFree
            to_bool(item_data.get('is_nut_free', False)),                 # isNutFre
            to_bool(item_data.get('is_low_carb', False)),                 # isLowCarb
            item_data.get('spiciness_level'),                    # spicinessLevel

            item_data.get('special_notes'),                      # specialNotes
            to_decimal(item_data.get('calories')),               # calories
            to_decimal(item_data.get('protein')),                # proteins
            to_decimal(item_data.get('carbs')),                  # carbs
            to_decimal(item_data.get('fat')),                    # fat
            to_decimal(item_data.get('fiber')),                  # fiber
            to_decimal(item_data.get('sugar')),                  # sugar
            to_decimal(item_data.get('sodium')),                 # sodium

            None,                                                # image (not provided)
            item_category_id,                                    # itemCategoryId
            menu_id,                                             # menuId
            location_id,                                       # locationSlug

            [],                                                  # optionGroupsOrder
            True,                                                # isActive
            None,                                                # posId
            None                                                 # backgroundInformation
        )

        cur.execute(
            """
            INSERT INTO item (
                id, name, short_description, full_description, price, currency, portion_size,
                cuisine_type, preparation_method,
                is_vegan, is_vegetarian, is_gluten_free, is_dairy_free,
                is_nut_free, is_low_carb, spiciness_level,
                special_notes, calories, proteins, carbs, fat, fiber, sugar, sodium,
                image, item_category_id, menu_id, location_id,
                option_groups_order, is_active, pos_id, background_information
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            ON CONFLICT (name, location_id, menu_id)
            DO UPDATE SET id = item.id
            RETURNING id;
            """,
            insert_row
        )

        item_id = cur.fetchone()[0]
        
        for ingredient_name in item_data.get("ingredients", []):
            cur.execute("""
                INSERT INTO ingredients (id, name, quantity, item_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                str(uuid.uuid4()),
                ingredient_name,
                None,            # no quantity provided in your JSON
                item_id          # FK to Item
            ))
        
        
        # Insert each allergen
        for allergen in item_data.get("allergens", []):
            cur.execute("""
                INSERT INTO allergens (id, name, item_id)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                str(uuid.uuid4()),
                allergen,
                item_id
            ))
    conn.commit()
    
        
        
        



cur.close()
conn.close()
