from dataclasses import dataclass
from typing import Callable
from airtable.web_requests import create_webhook, delete_webhook
from database import engine
from sqlalchemy import text
import os

HOST = os.getenv('HOST')


@dataclass
class AutomationWebhook:
    fields: [str]
    includes: [str]
    func: Callable


class Automation:
    def __init__(self, base_id, table_id):
        self.base_id = base_id
        self.table_id = table_id
        self.automation_list = []

    def automation(self, fields=None, includes=None):
        def decorator(f):
            self.automation_list.append(AutomationWebhook(fields=fields, includes=includes, func=f))
            return f

        return decorator

    def create_mapping(self):
        webhook_to_delete = []
        webhook_to_create = self.automation_list.copy()

        with engine.connect() as conn:
            records = conn.execute(text(
                '''
                SELECT webhook_id, func FROM mappings
                '''
            ))

            for row in records:
                if not any(x.func.__name__ == row.func for x in self.automation_list):
                    webhook_to_delete.append((row.webhook_id, row.func))
                webhook_to_create.remove(next(x for x in self.automation_list if x.func.__name__ == row.func))

            for record in webhook_to_delete:
                delete_webhook(self.base_id, record[0])
                conn.execute(text(
                    '''
                    DELETE FROM mappings 
                    WHERE webhook_id = '{webhook_id}' AND func='{func}'
                    '''.format(webhook_id=record[0], func=record[1])
                ))
                print(f"Deleted webhook {record[0]} associated with {record[1]}")

            for record in webhook_to_create:
                res = create_webhook(self.base_id, f'https://{HOST}/notification', self.table_id, fields=record.fields, includes=record.includes)
                id = res['id']
                conn.execute(text(
                    '''
                    INSERT INTO mappings (id, webhook_id, func) 
                    VALUES(DEFAULT, '{webhook_id}', '{func}')
                    '''.format(webhook_id=id, func=record.func.__name__)
                ))
                print(f"Created webhook {id} associated with {record.func.__name__}")
