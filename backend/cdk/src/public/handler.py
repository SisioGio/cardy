
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from shared.models.item import Item
from utils import get_secret

load_dotenv()


DB_SECRET_CRED_NAME = os.getenv("RDS_SECRET_NAME")
DB_CREDENTIALS = get_secret(DB_SECRET_CRED_NAME)
DB_ENDPOINT=os.getenv("DB_ENDPOINT")
DB_DATABASE = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f'postgresql+psycopg2://{DB_CREDENTIALS['username']}:{DB_CREDENTIALS['password']}@{DB_ENDPOINT}:{DB_PORT}/{DB_DATABASE}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
def lambda_handler(event, context):



    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"message": "Hello from public2"}'
    }
