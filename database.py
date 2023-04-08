import os
from sqlalchemy import create_engine

RAW_DB_URL = os.getenv('DATABASE_URL')
DATABASE_URL = RAW_DB_URL.replace('postgres://', 'postgresql+psycopg2://', 1)

engine = create_engine(DATABASE_URL)