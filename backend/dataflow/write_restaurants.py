import pandas as pd
import json
import psycopg2
from slugify import slugify
import uuid
from datetime import datetime
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

# --------------------------
# Read Excel
# --------------------------
df = pd.read_excel(r"C:\Users\Alessio\Projects\cardy-dev\dataflow\static\restaurant_12112025.xlsx")
df['about'] = df['about'].fillna('[]')
df['other_hours'] = df['other_hours'].fillna('[]')

df['working_hours'] = df['working_hours'].fillna('{}')
# --------------------------
# Helper to flatten 'about'
# --------------------------
def flatten_about(obj, prefix=""):
    entries = []
    for k, v in obj.items():
        if isinstance(v, dict):
            entries.extend(flatten_about(v, f"{prefix}{k} > "))
        else:
            entries.append((f"{prefix}{k}", str(v)))
    return entries


def get_priceRange(row):
    if pd.isna(row['range']):
        return None
    else:
        return len(row['range'])
    
def get_all_emails(df, row):
    emails = df[df['site'] == row['site']]['email']
    return emails.dropna().tolist()

def parse_time(time_str):
    s = time_str.strip().lower()

    # Handle empty or invalid
    if not s:
        return None

    # Add minutes if missing
    if ':' not in s:
        if 'am' in s or 'pm' in s:
            s = s.replace('am', ':00am').replace('pm', ':00pm')
        else:
            s += ':00'  # assume 24-hour if AM/PM missing

    # Add AM if only hour provided without AM/PM (assuming morning)
    if s.replace(':', '').isdigit():
        s += 'am'

    # Try multiple formats
    formats = ["%I:%M%p", "%I:%M %p", "%H:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).time()
        except ValueError:
            continue

    # If all fail, return None
    return None

# --------------------------
# Loop through rows
# --------------------------

df = df.where(pd.notnull(df), None)
for _, row in df.iterrows():
    try:
        # 1️⃣ Company
        company_name = row.get("name") if pd.notna(row.get("name")) else 'unknown-company-name'

        company_slug = slugify(company_name)
        
        location_name = company_name +"-"+row.get("street") if not pd.isna(row.get("street")) else row.get("full_address")
        location_slug = slugify(location_name)
        cur.execute("""
            SELECT COUNT(*) FROM location WHERE slug = %s
        """, (location_slug,))

        count = cur.fetchone()[0]  # fetchone returns a tuple
        if count > 0:
            # print(f"Skipping {location_name}, slug {location_slug} already exists ✅")
            continue
        
        
        cur.execute("""
            INSERT INTO company (id,name, slug)
            VALUES (%s,%s, %s)
            ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name
            RETURNING slug
        """, (str(uuid.uuid4()),company_name, company_slug))
        company_slug_db = cur.fetchone()[0]

        # 2️⃣ Location
        
        location_emails = get_all_emails(df,row)
        price_range = get_priceRange(row)
        cur.execute("""
            INSERT INTO location (
                id,  name, slug, company_slug, location_name,
                reviews_link, site, subtypes, category, type,
                company_phone, company_phones, company_facebook, company_instagram,
                email, latitude, longitude, time_zone, rating, photos_count,
                photo, price_range, owner_id, reservation_link, booking_link,
                order_link, location_link, place_id, google_id
            )
            VALUES (
                %s, %s, %s, %s,%s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id
        """, (
            str(uuid.uuid4()),
            location_name,
            location_slug,
            company_slug_db,
            company_name,
            
            
            row.get("reviews_link") or "",
            row.get("site") or "",
            [s.strip() for s in str(x).split(",") if s.strip()]
                if (x := row.get("subtypes")) and not pd.isna(x)
                else [],
            row.get("category") or "",
            row.get("type") or "",
            
            
            row.get("company_phone") or "",
            row.get("company_phones").split(",") if not pd.isna(row.get("company_phones")) else [],
            row.get("company_facebook") or "",
            row.get("company_instagram") or "",
            
            
            location_emails,
            row.get("latitude") or None,
            row.get("longitude") or None,
            row.get("time_zone") or "",
            row.get("rating") or None,
            row.get("photos_count") if not pd.isna(row.get("photos_count")) else 0,
            
            
            row.get("photo") or "",
            price_range,
            row.get("owner_id") or "",
            row.get("reservation_links") or "",
            row.get("booking_appointment_link") or "",
            
            
            row.get("order_links") or "",
            row.get("location_link") or "",
            row.get("place_id") or "",
            row.get("google_id") or "",
        ))
        location_id = cur.fetchone()[0]

        # 3️⃣ Working Hours
        working_hours_str = row.get("working_hours") or "{}"
        wh = json.loads(working_hours_str)
        for day, hours in wh.items():
            is_closed = str(hours).lower() == "closed"
            open_time = close_time = None
            if not is_closed and "-" in hours:
                parts = hours.split("-")
                open_time = parts[0].strip()
                close_time = parts[1].strip()
                open_time = parse_time(open_time)
                close_time = parse_time(close_time)
            cur.execute("""
                INSERT INTO location_working_hours (id,location_id, day_of_week, open_time, close_time, is_closed)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (str(uuid.uuid4()),location_id, day, open_time, close_time, is_closed))

        # 4️⃣ Takeout Hours (optional)
        other_hours = row.get("other_hours") or "[]"
        other_hours = json.loads(other_hours)
        for line in other_hours:
            for key,value in line.items():
                for day,value in value.items():
                    is_closed = str(value).lower() == "closed"
                    open_time = close_time = None
                    if not is_closed and "-" in hours:
                        parts = value.split("-")
                        open_time = parts[0].strip()
                        close_time = parts[1].strip()
                        open_time = parse_time(open_time)
                        close_time = parse_time(close_time)
                    cur.execute("""
                        INSERT INTO location_other_hours (id,location_id,category, day_of_week, open_time, close_time,is_closed)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, (str(uuid.uuid4()),location_id,key, day, open_time, close_time, is_closed))
            
            
        

        # 5️⃣ About
        about_str = row.get("about")
   
        if about_str and not pd.isna(about_str):
            about_obj = json.loads(about_str)
            # flattened = flatten_about(about_obj)
            for category, items in about_obj.items():
                for key,value in items.items():
                    if not isinstance(value, bool):
                        continue
                   
                        
                    cur.execute("""
                        INSERT INTO location_about (id,location_id,category, key, value)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (str(uuid.uuid4()),location_id,category, key, value))
                   
        
        print(f"✅ Imported: {location_name}")
        conn.commit()
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error importing {row.get('name')}: {e}")
        print(f"  pgcode: {e.pgcode}")
        print(f"  pgerror: {e.pgerror}")
        print(f"  diag: {e.diag}")  # more details, like constraint name
    except Exception as e:
        conn.rollback()
        print(f"❌ Error importing {row.get('name')}: {e}")

# --------------------------
# Close connection
# --------------------------
cur.close()
conn.close()
