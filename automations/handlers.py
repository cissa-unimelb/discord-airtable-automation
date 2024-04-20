from automations.types import Automation
from automations.utils import *
from discord_api.web_requests import *
import os
import datetime

PUB_URL = os.getenv('PUBLICITY_HOOK_URL')
UMSU_URL = os.getenv('UMSU_HOOK_URL')
BASE_ID = os.getenv('BASE_ID')
TABLE_ID = os.getenv('TABLE_ID')
# TODO: Find a better way to automate airtable->discord mappings
DISCORD_MAPPINGS = {
    # Newsletter officer
    "Delia Zhou": "649597957993398277",

    # Creative content officer
    "Zita Lam": "781782653148987454",

    # Design officers
    "Amy Nguyen": "464366290195447828",
    "Lihini Gamage": "504697814190784532",
    "Megane Boucherat": "766532985797083137",
    "Vidhya Kudikyala": "690380645830230016",
    "Hyun-jin Park": "379580395844534273",

    # Execs and directors
    "Kasie Wang": "827474078386225152",
    "Sean Khoo": "231371639638458368",
    "Margaret Xu": "718760476343009332",
    # "Aarushi Dua": "698046487233560586",

    # IT officers
    "Michael Ren": "1138969490432991232",
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
                    send_message(PUB_URL, f'A new record has been added: **{record.name}** ({activity_type_name}) in {week_name} \nCC: <@698046487233560586>')
                    print(f'Activity: {record.name} has been made')


@automation.automation(fields=['fld8OuJdShG0Q4laa'])
def update_date(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            for field in record.fields:
                if field.id == 'fld8OuJdShG0Q4laa' and field.curr is not None:
                    add_matched(webhook_id, record.id)
                    send_message(PUB_URL, f'Date for **{record.name}** is now {parse_time(field.curr)}. \nCC: <@698046487233560586>')
                    print(f'The date of {record.name} has been updated to {parse_time(field.curr)}')


@automation.automation(fields=['fldESRtthFAGdQhwL'], includes=['fldzkN3GrrQbeC2JI', 'fld4zvgvNx6EjYXGG', 'fldnHVl2usXCGUxk0'])
def facebook_publicity_warnings(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            has_fb_link = False
            overdue = False
            pub_ddl = None
            no_fb_required = False

            for field in record.fields:
                if field.id == 'fldESRtthFAGdQhwL' and field.curr is not None:
                    if int(field.curr) >= 0:
                        overdue = True
                elif field.id == 'fldzkN3GrrQbeC2JI' and field.curr is not None:
                    has_fb_link = True
                elif field.id == 'fld4zvgvNx6EjYXGG' and field.curr is not None:
                    pub_ddl = field.curr
                elif field.id == 'fldnHVl2usXCGUxk0' and field.curr is not None:
                    no_fb_required = True

            if overdue and not has_fb_link and not no_fb_required:
                send_message(PUB_URL,
                             f'Please create Facebook event for **{record.name}** by {pub_ddl}. \nCC: <@698046487233560586>')
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


@automation.automation(fields=['fldYAhf3IO3lgPYmu'], includes=['fldvfYt7UlFsyprdL', 'fldATjzozdbU5f6KJ', 'fldOIlEMi83OwCKqt'])
def umsu_grant_warnings(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            has_umsu_grant = False
            overdue = False
            grant_ddl = None
            no_umsu_required = False

            for field in record.fields:
                if field.id == 'fldvfYt7UlFsyprdL' and field.curr is not None:
                    has_umsu_grant = True
                elif field.id == 'fldYAhf3IO3lgPYmu' and field.curr is not None:
                    if int(field.curr) >= 0:
                        overdue = True
                elif field.id == 'fldATjzozdbU5f6KJ' and field.curr is not None:
                    grant_ddl = field.curr
                elif field.id == 'fldOIlEMi83OwCKqt' and field.curr is not None:
                    no_umsu_required = True

            if overdue and not has_umsu_grant and not no_umsu_required:
                send_message(UMSU_URL,
                             f'Please apply for UMSU Grant for **{record.name}** before 11.59pm, {grant_ddl}. \nCC: <@998269811584938005>')
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
                             f'Please upload attendance sheet for **{record.name}**. \nCC: <@198255674818297856>')
                print(f'Attendance sheet warning for {record.name} has been sent')


@automation.automation(fields=['fldndprPs52tyQ35m', 'fld8OuJdShG0Q4laa', 'fldUKQ4EXpwS7QmYA', 'fldBB5DRsNzvsNb0n', 'fld0amHJcvTUM3q4r', 'fld2Sp7IHpZx50zG1', 'fldDzpbCxGXXpzGZy'], includes=['fldndprPs52tyQ35m', 'fld8OuJdShG0Q4laa', 'fldUKQ4EXpwS7QmYA', 'fldBB5DRsNzvsNb0n', 'fld0amHJcvTUM3q4r', 'fld2Sp7IHpZx50zG1', 'fldDzpbCxGXXpzGZy'])
def discord_events(webhook_id, payloads):
    for payload in payloads:
        for record in payload.changed_records:
            name = None
            start_date = None
            end_date = None
            venue = None
            image = None
            event_type = None
            date_confirmed = False

            for field in record.fields:
                if field.id == 'fldndprPs52tyQ35m' and field.curr is not None:
                    name = field.curr
                elif field.id == 'fld8OuJdShG0Q4laa' and field.curr is not None:
                    start_date = datetime.datetime.strptime(field.curr, '%Y-%m-%dT%H:%M:%S.%fZ')
                elif field.id == 'fldUKQ4EXpwS7QmYA' and field.curr is not None:
                    end_date = field.curr
                elif field.id == 'fldBB5DRsNzvsNb0n' and field.curr is not None:
                    venue = field.curr
                elif field.id == 'fld0amHJcvTUM3q4r' and field.curr is not None:
                    image = field.curr
                elif field.id == 'fld2Sp7IHpZx50zG1' and field.curr is not None:
                    event_type = field.curr['name']
                elif field.id == 'fldDzpbCxGXXpzGZy' and field.curr is not None:
                    date_confirmed = field.curr

            if start_date is not None and end_date is not None:
                end_date = start_date + datetime.timedelta(seconds=int(end_date))
            if image is not None:
                image = image_to_data_uri(image[0]['url'])

            if start_date is not None and end_date is not None and \
                    start_date > datetime.datetime.utcnow() and venue is not None and \
                    date_confirmed and event_type is not None and event_type != "People & Culture":
                start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                if update_event(record.id, name, None, start_date, end_date, venue, image) is not None:
                    print(f'{name} discord event has been updated')
                else:
                    create_event(record.id, name, None, start_date, end_date, venue, image)
                    print(f'{name} discord event has been created')
