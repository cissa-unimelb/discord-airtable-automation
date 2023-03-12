from config import IS_PROD
import os
from sqlalchemy import create_engine

if not IS_PROD:
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.getenv('LOCAL_DB')
else:
    DATABASE_URL = os.getenv('PROD_DB')

engine = create_engine(DATABASE_URL)