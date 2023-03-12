from config import IS_PROD
import os
import requests
from airtable.types import *
from database import engine
from sqlalchemy import text
from airtable.utils import collect_fields, prune
from datetime import datetime

if not IS_PROD:
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv('ACCESS_TOKEN')
NAME_FIELD_ID = 'fldndprPs52tyQ35m'


def list_webhooks(base_id):
    url = f'https://api.airtable.com/v0/bases/{base_id}/webhooks'
    req = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    arr = req.json()
    return [Webhook(
        id=res['id'],
        cursor_for_next_payload=res['cursorForNextPayload'],
        is_hook_enabled=res['isHookEnabled'],
        notification_url=res['notificationUrl'],
        expiration_time=res['expirationTime'],
        specification=WebhookSpecification(
            filters=WebhookSpecFilter(
                data_type=res['specification']['options']['filters']['dataTypes'],
                record_change_scope=res['specification']['options']['filters']['recordChangeScope'],
                watch_data_in_field_ids=None if 'watchDataInFieldIds' not in res['specification']['options'][
                    'filters'] else res['specification']['options']['filters']['watchDataInFieldIds']
            ),
            includes=WebhookSpecInclude(
                include_cell_values_in_field_ids=None if 'includeCellValuesInFieldIds' not in
                                                         res['specification']['options']['includes'] else
                res['specification']['options']['includes']['includeCellValuesInFieldIds'],
                include_previous_cell_values=res['specification']['options']['includes']['includePreviousCellValues']
            )
        )
    ) for res in arr['webhooks']]


def create_webhook(base_id, url, table_id, fields=None, includes=None):
    if includes is None:
        includes = [NAME_FIELD_ID]
    else:
        includes.append(NAME_FIELD_ID)

    api_url = f'https://api.airtable.com/v0/bases/{base_id}/webhooks'
    body = {
        "notificationUrl": url,
        "specification": {
            "options": {
                "filters": {
                    "dataTypes": ["tableData"],
                    "recordChangeScope": table_id,
                    "watchDataInFieldIds": fields
                },
                "includes": {
                    "includeCellValuesInFieldIds": includes,
                    "includePreviousCellValues": True
                }
            }
        }
    }

    if fields is None:
        del body["specification"]["options"]["filters"]["watchDataInFieldIds"]

    req = requests.post(api_url, headers={'Authorization': f'Bearer {TOKEN}'}, json=body)
    res = req.json()

    with engine.connect() as conn:
        records = conn.execute(text(
            '''
        SELECT 1 FROM WEBHOOKS WHERE WEBHOOK_ID = '{webhook_id}'
        '''.format(webhook_id=res['id'])
        )).all()
        if len(records) == 0:
            conn.execute(text(
                '''
                INSERT INTO webhooks (id, webhook_id, last_cursor)
                VALUES(DEFAULT, '{webhook_id}', 1);
                '''.format(webhook_id=res['id'])
            ))

    return res


def list_webhook_payloads(base_id, webhook_id, table_id):
    url = f'https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads'
    req = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    resp = req.json()

    while resp['mightHaveMore']:
        url = f'https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}/payloads?cursor={resp["cursor"]}'
        req = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
        resp = req.json()

    res = []

    with engine.connect() as conn:
        result = conn.execute(text(
            '''
            SELECT last_cursor FROM webhooks
            WHERE webhook_id = '{webhook_id}';
            '''.format(webhook_id=webhook_id)
        ))
        for row in result:
            num_new = int(resp['cursor']) - int(row.last_cursor)
        conn.execute(text(
            '''
            UPDATE webhooks
            SET last_cursor = {curr_cursor}
            WHERE webhook_id = '{webhook_id}';
            '''.format(curr_cursor=resp['cursor'], webhook_id=webhook_id)
        ))

    if num_new == 0:
        return []

    for payload in resp['payloads'][-num_new:]:
        tbl_payload = payload['changedTablesById'][table_id]
        changed = list(map(collect_fields,
                           tbl_payload['changedRecordsById'].items())) if 'changedRecordsById' in tbl_payload else None
        created = list(map(collect_fields,
                           tbl_payload['createdRecordsById'].items())) if 'createdRecordsById' in tbl_payload else None

        res.append(WebhookPayload(timestamp=datetime.strptime(payload['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ'), changed_records=changed, created_records=created))

    return prune(res)


def delete_webhook(base_id, webhook_id):
    url = f'https://api.airtable.com/v0/bases/{base_id}/webhooks/{webhook_id}'
    res = requests.delete(url, headers={'Authorization': f'Bearer {TOKEN}'})
    return res.json()



