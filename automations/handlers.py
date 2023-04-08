from automations.types import Automation
from automations.utils import *
import os

PUB_URL = os.getenv('PUBLICITY_HOOK_URL')
UMSU_URL = os.getenv('UMSU_HOOK_URL')
BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')

automation = Automation(BASE_ID, TABLE_ID)


@automation.automation(fields=['fldUKQ4EXpwS7QmYA', 'fldBB5DRsNzvsNb0n'])
def duration_n_venue3(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            print(f"Activity: {record.name}'s location has been updated to {record.fields[0].curr}")
    return None


@automation.automation(fields=['fldndprPs52tyQ35m', 'fld2Sp7IHpZx50zG1', 'fldcyH6xTBPFHxVXo'], includes=['fld2Sp7IHpZx50zG1', 'fldcyH6xTBPFHxVXo'])
def new_event_created(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            name = False
            activity_type = False
            activity_type_name = None
            week = False
            week_name = None

            for field in record.fields:
                if field.id == 'fldndprPs52tyQ35m' and field.curr is not None:
                    name = True
                if field.id == 'fld2Sp7IHpZx50zG1' and field.curr is not None:
                    activity_type = True
                    activity_type_name = field.curr['name']
                if field.id == 'fldcyH6xTBPFHxVXo' and field.curr is not None:
                    week = True
                    week_name = field.curr['name']

            if name and activity_type and week:
                if has_not_matched(webhook_id, record.id):
                    add_matched(webhook_id, record.id)
                    send_message(PUB_URL, f'A new record has been added: **{record.name}** ({activity_type_name}) in {week_name} \n CC: <@277373956582014977>')
                    print(f'Activity: {record.name} has been made')


automation.create_mapping()