from sqlalchemy import text
from migrations.config import engine

with engine.connect() as conn:
    conn.execute(text(
        '''
        CREATE TABLE matched_records(
            ID SERIAL PRIMARY KEY,
            WEBHOOK_ID VARCHAR(100),
            RECORD_ID VARCHAR(100)
        );
        '''
    ))

    print("Schema", conn.execute(text(
        '''
        SELECT table_name, column_name, data_type FROM information_schema.columns
        WHERE table_name = 'matched_records';
        '''
    )).all())