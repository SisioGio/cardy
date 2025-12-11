from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy.sql import expression as expr
from sqlalchemy import func
def time_to_str(t):
    return t.strftime("%H:%M") if t else None

def parse_time(value):
    if value is None or str(value).strip() == "":
        return None
    
    value = str(value).strip().lower()

    # Handle values like "4" → assume it's 4:00
    if value.isdigit():
        value += ":00"

    # Try multiple formats
    time_formats = [
        "%I:%M%p",   # 10:00am
        "%I%p",      # 7am
        "%H:%M",     # 17:00
        "%I:%M %p",  # 10:00 am
        "%H",        # 4
    ]

    for fmt in time_formats:
        try:
            return datetime.strptime(value, fmt).time()
        except Exception:
            continue

    print(f"❌ Could not convert {value} into time format")
    return None


def parse_boolean(val: str):
    val = val.strip().lower()
    if val in ["true", "1", "yes"]:
        return True
    if val in ["false", "0", "no"]:
        return False
    return None


def apply_dynamic_filters(query, model, config, join_model=None):
    for param, rule in config.items():
        raw_value = request.args.get(param)
        if raw_value is None:
            continue

        # Use join model if provided (like LocationWorkingHours)
        target_model = join_model if join_model else model
        column = getattr(target_model, rule["attribute"])
        print(f"Applying filter on {rule['attribute']} {rule['operator']} {raw_value}")
        ### STRING ###
        if rule["type"] == "string":
            if rule["operator"] == "contains":
                query = query.filter(column.ilike(f"%{raw_value}%"))
            else:  # eq
                query = query.filter(func.lower(column) == raw_value.lower())

        ### NUMBER ###
        elif rule["type"] == "number":
            # --- Range filter ---
            if rule.get("operator") == "range":
                min_val = request.args.get(f"{param}_min", type=float)
                max_val = request.args.get(f"{param}_max", type=float)

                if min_val is not None:
                    print(f"Querying {param}_min: {min_val}")
                    query = query.filter(column >= min_val)
                if max_val is not None:
                    query = query.filter(column <= max_val)

            # --- Fallback for single value ---
            elif raw_value is not None:
                try:
                    value = float(raw_value)
                    if rule.get("operator") == "gte":
                        query = query.filter(column >= value)
                    elif rule.get("operator") == "lte":
                        query = query.filter(column <= value)
                    else:
                        query = query.filter(column == value)
                except ValueError:
                    # Ignore invalid numeric input
                    continue


        ### TIME ###
        elif rule["type"] == "time":
            value = parse_time(raw_value)
            print(f"Checking {value} for {column} op {rule['operator']}")
            if not value:
                continue

            if rule["operator"] == "gte":
                query = query.filter(column >= value)
            elif rule["operator"] == "lte":
                query = query.filter(column <= value)

        ### BOOL ###
        elif rule["type"] == "bool":
            val = parse_boolean(raw_value)
            print(f"Boolean value: {val}")
            query = query.filter(column == val)

    return query

