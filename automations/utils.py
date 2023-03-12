from database import engine
from sqlalchemy import text
import requests


def has_not_matched(webhook_id, record_id):
    with engine.connect() as conn:
        res = conn.execute(text(
            '''
            SELECT 1 FROM matched_records
            WHERE webhook_id='{webhook_id}' AND record_id='{record_id}';
            '''.format(webhook_id=webhook_id, record_id=record_id)
        ))

        return len(res.all()) == 0


def add_matched(webhook_id, record_id):
    with engine.connect() as conn:
        conn.execute(text(
            '''
            INSERT INTO matched_records (id, webhook_id, record_id) 
            VALUES(DEFAULT, '{webhook_id}',  '{record_id}');
            '''.format(webhook_id=webhook_id, record_id=record_id)
        ))


def send_message(url, message):
    requests.post(url, json={'content':message})