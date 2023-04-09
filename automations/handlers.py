from automations.types import Automation
from automations.utils import *
import os
import datetime

PUB_URL = os.getenv('PUBLICITY_HOOK_URL')
UMSU_URL = os.getenv('UMSU_HOOK_URL')
BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')
# TODO: Find a better way to automate airtable->discord mappings
DISCORD_MAPPINGS = {
    "Catherine Muir": "274879451689517056",
    "Harry Chen": "425974501600395265",
    "Ivan Zhuang": "277373956582014977",
    "Rebecca Hwang": "481421416902819848",
    "Stella Li": "255956057774358528",
    "Vidhya Kudikyala": "690380645830230016",
    "Kasie Wang": "827474078386225152",
    "Florence Tang": "737253087680528384",
    "Gunjan Ahluwalia": "1074325276487589979",
    "Elysia Lelon": "755747243167842365"
}

automation = Automation(BASE_ID, TABLE_ID)


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


@automation.automation(fields=['fld8OuJdShG0Q4laa'])
def update_date(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            for field in record.fields:
                if field.id == 'fld8OuJdShG0Q4laa' and field.curr is not None:
                    add_matched(webhook_id, record.id)
                    send_message(PUB_URL, f'Date for **{record.name}** is now {parse_time(field.curr)}. \n CC: <@277373956582014977>')
                    print(f'The date of {record.name} has been updated to {parse_time(field.curr)}')


@automation.automation(fields=['fldESRtthFAGdQhwL'], includes=['fldzkN3GrrQbeC2JI', 'fld4zvgvNx6EjYXGG'])
def facebook_publicity_warning(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            has_fb_link = False
            overdue = False
            pub_ddl = None

            for field in record.fields:
                if field.id == 'fldESRtthFAGdQhwL' and field.curr is not None:
                    if int(field.curr) >= 0:
                        overdue = True
                elif field.id == 'fldzkN3GrrQbeC2JI' and field.curr is not None:
                    has_fb_link = True
                elif field.id == 'fld4zvgvNx6EjYXGG' and field.curr is not None:
                    pub_ddl = field.curr

            if overdue and not has_fb_link:
                send_message(PUB_URL,
                             f'Please create Facebook event for **{record.name}** by {pub_ddl}. \n CC: <@277373956582014977>')
                print(f'Facebook publicity warning for {record.name} has been sent')


@automation.automation(fields=['fldItkLW4MbQF2uqZ'], includes=['fld4zvgvNx6EjYXGG'])
def update_description_assignee(webhook_id, payloads):
    discord_id = None
    pub_ddl = None

    for payload in payloads:
        for record in payload.changed_records:
            for field in record.fields:
                if field.id == 'fldItkLW4MbQF2uqZ' and field.curr is not None:
                    discord_id = DISCORD_MAPPINGS[field.curr['name']] if field.curr['name'] in DISCORD_MAPPINGS else field.curr['name']
                elif field.id == 'fld4zvgvNx6EjYXGG' and field.curr is not None:
                    pub_ddl = field.curr

            new_pub_ddl = datetime.datetime.strptime(pub_ddl, '%B %d, %Y') - datetime.timedelta(days=2)
            send_message(PUB_URL,
                         f'<@{discord_id}>, you have been assigned to **{record.name}** due {new_pub_ddl.strftime("%B %d, %Y")}.')
            print(f'Description assignee for {record.name} has been updated')


@automation.automation(fields=['fld2qIwlSwJkvKT74'], includes=['fld4zvgvNx6EjYXGG'])
def update_graphics_assignee(webhook_id, payloads):
    discord_id = None
    pub_ddl = None

    for payload in payloads:
        for record in payload.changed_records:
            for field in record.fields:
                if field.id == 'fld2qIwlSwJkvKT74' and field.curr is not None:
                    discord_id = DISCORD_MAPPINGS[field.curr['name']] if field.curr['name'] in DISCORD_MAPPINGS else field.curr['name']
                elif field.id == 'fld4zvgvNx6EjYXGG' and field.curr is not None:
                    pub_ddl = field.curr

            new_pub_ddl = datetime.datetime.strptime(pub_ddl, '%B %d, %Y') - datetime.timedelta(days=2)
            send_message(PUB_URL,
                         f'<@{discord_id}>, you have been assigned to **{record.name}** due {new_pub_ddl.strftime("%B %d, %Y")}.')
            print(f'Graphics assignee for {record.name} has been updated')


@automation.automation(fields=['fldYAhf3IO3lgPYmu'], includes=['fldvfYt7UlFsyprdL', 'fldATjzozdbU5f6KJ'])
def umsu_grant_warning(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            has_umsu_grant = False
            overdue = False
            grant_ddl = None

            for field in record.fields:
                if field.id == 'fldvfYt7UlFsyprdL' and field.curr is not None:
                    has_umsu_grant = True
                elif field.id == 'fldYAhf3IO3lgPYmu' and field.curr is not None:
                    if int(field.curr) >= 0:
                        overdue = True
                elif field.id == 'fldATjzozdbU5f6KJ' and field.curr is not None:
                    grant_ddl = field.curr

            if overdue and not has_umsu_grant:
                send_message(UMSU_URL,
                             f'Please apply for UMSU Grant for **{record.name}** before 11.59pm, {grant_ddl}. \n CC: <@561750831448457237>')
                print(f'UMSU Grant warning for {record.name} has been sent')


@automation.automation(fields=['fldDS4LxkqZYlIq6y'], includes=['fld2Sp7IHpZx50zG1', 'fldvGA92TGK1YXtSe'])
def attendence_sheet_warning(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            has_attendance_sheet = False
            overdue = False
            event_type = None

            for field in record.fields:
                if field.id == 'fldvGA92TGK1YXtSe' and field.curr is not None:
                    has_attendance_sheet = True
                elif field.id == 'fldDS4LxkqZYlIq6y' and field.curr is not None:
                    if int(field.curr) == 3:
                        overdue = True
                elif field.id == 'fld2Sp7IHpZx50zG1' and field.curr is not None:
                    event_type = field.curr

            if overdue and not has_attendance_sheet and event_type['name'] != 'People & Culture':
                send_message(UMSU_URL,
                             f'Please upload attendance sheet for **{record.name}**. \n CC: <@1001264127555141642>')
                print(f'Attendance sheet warning for {record.name} has been sent')