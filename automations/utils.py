from database import engine
from sqlalchemy import text
import requests
import pytz
from datetime import datetime
import base64


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


def parse_time(time):
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    time = time.replace(tzinfo=pytz.utc)
    time = time.astimezone(pytz.timezone('Australia/Melbourne'))
    return time.strftime('%d/%m/%Y %H:%M:%S')


def image_to_data_uri(image_url):
    res = requests.get(image_url)
    content_type = res.headers['Content-Type']
    b64str = base64.b64encode(res.content).decode('utf-8')
    return f"data:{content_type};base64,{b64str}"