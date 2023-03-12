from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

PROD_MIGRATIONS = False # Set this flag to true when running migrations on prod db

load_dotenv()
if PROD_MIGRATIONS:
    engine = create_engine(os.getenv('PROD_DB'))
else:
    engine = create_engine(os.getenv('LOCAL_DB'))