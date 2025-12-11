import os

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Jkd>4ou]8~([[GUcvdGut):*>WFk")
DB_HOST = os.environ.get("DB_HOST", "cardy-dev.cb60yy2s4a4i.eu-central-1.rds.amazonaws.com")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
