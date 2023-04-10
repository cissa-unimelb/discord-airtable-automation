import os

from flask import Blueprint, request
from airtable.web_requests import list_webhook_payloads
from database import engine
from sqlalchemy import text

controllers = Blueprint('controllers', __name__)
BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')


@controllers.route('/', methods=['GET'])
def hello():
    return 'world'


@controllers.route('/notification', methods=['POST'])
def notification():
    webhook_id = request.json['webhook']['id']
    print(f"Received webhook {webhook_id}")
    func_name = None
    with engine.connect() as conn:
        res = conn.execute(text(
            '''
            SELECT func FROM mappings
            WHERE mappings.webhook_id = '{webhook_id}'
            '''.format(webhook_id=webhook_id)
        ))

        for row in res:
            func_name = row.func

    if func_name is None:
        print(f"No webhook mapping exist with webhook {webhook_id}")
    else:
        print(f"Executing {func_name} with webhook {webhook_id}")
        payloads = list_webhook_payloads(BASE_ID, webhook_id, TABLE_ID)
        exec(f'from automations.handlers import {func_name}\n{func_name}("{webhook_id}", payloads)')

    return 'null'
