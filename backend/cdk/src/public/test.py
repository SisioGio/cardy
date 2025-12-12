import sys
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from handler import lambda_handler


res=lambda_handler({'queryStringParameters':{
    'lat':48.07,
    'lng':11.52,
    'range':10,
 
    'paginate':"true",
    'page':"1",
    'page_size':"5"
    
    }},{})

print(json.loads(res['body'])['total'])
print(json.loads(res['body'])['curr_total'])
# print(json.loads(res['body']))

