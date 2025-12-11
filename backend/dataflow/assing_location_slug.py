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

file_path = r'C:\Users\Alessio\Projects\cardy-dev\dataflow\static\output_12112025.json'

with open(file_path,'rb') as f:
    restaurants=json.load(f)
    
    
def find_slug(cur,name,site):
    cur.execute(
        """SELECT l.id
                FROM location AS l
                JOIN company AS c ON l.company_slug = c.slug
                WHERE c.name = %s or l.site = %s""",
        (name,site))
    result = cur.fetchone()
    if not result:
        print(f"Could not find restaurant {name}  url {site} in database")
        return None
    
    location_id = result[0]
    return location_id

for row in restaurants:
    
    location_id = find_slug(cur,row['name'],row['site'])
    row['id'] = location_id
    
with open(r'C:\Users\Alessio\Projects\cardy\backend\dataflow\static\output_29112025.json','w') as f:
    json.dump(restaurants,f)
    
