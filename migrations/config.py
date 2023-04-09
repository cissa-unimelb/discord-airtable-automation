from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

PROD_MIGRATIONS = False # Set this flag to true when running migrations on prod db

load_dotenv()
if PROD_MIGRATIONS:
    DB_URL = os.getenv('PROD_DB')
else:
    DB_URL = os.getenv('DATABASE_URL')

engine = create_engine(DB_URL.replace('postgres://', 'postgresql+psycopg2://', 1))