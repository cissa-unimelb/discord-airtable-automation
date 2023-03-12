from sqlalchemy import text
from migrations.config import engine

with engine.connect() as conn:
    conn.execute(text(
        '''
        CREATE TABLE MAPPINGS(
            ID SERIAL,
            WEBHOOK_ID VARCHAR(50) NOT NULL,
            FUNC VARCHAR(100) NOT NULL UNIQUE,
            PRIMARY KEY (ID)
        );
        '''
    ))

    print("Schema", conn.execute(text(
        '''
        SELECT table_name, column_name, data_type FROM information_schema.columns
        WHERE table_name = 'mappings';
        '''
    )).all())