from sqlalchemy import text
from migrations.config import engine

with engine.connect() as conn:
    conn.execute(text(
        '''
        CREATE TABLE discord_event_mappings(
            ID SERIAL PRIMARY KEY,
            RECORD_ID VARCHAR(100),
            EVENT_ID VARCHAR(100)
        );
        '''
    ))

    print("Schema", conn.execute(text(
        '''
        SELECT table_name, column_name, data_type FROM information_schema.columns
        WHERE table_name = 'discord_event_mappings';
        '''
        )).all())