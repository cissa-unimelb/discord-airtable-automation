from sqlalchemy import text
from migrations.config import engine

with engine.connect() as conn:
    conn.execute(text(
        '''
        CREATE TABLE WEBHOOKS(
            ID SERIAL,
            WEBHOOK_ID VARCHAR(50) NOT NULL,
            LAST_CURSOR INT NOT NULL,
            PRIMARY KEY (ID)
        );
        '''
    ))

    print("Schema", conn.execute(text(
        '''
        SELECT table_name, column_name, data_type FROM information_schema.columns
        WHERE table_name = 'webhooks';
        '''
    )).all())
