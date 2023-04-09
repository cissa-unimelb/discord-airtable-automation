import requests
import os
from discord_api.types import *
from database import engine
from sqlalchemy import text

BASE_URL = "https://discord.com/api/v10"
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")


def send_message(url, message):
    requests.post(url, json={'content': message})


def list_events():
    headers = {
        'Authorization': f"Bot {DISCORD_TOKEN}"
    }
    res = requests.get(f"{BASE_URL}/guilds/{DISCORD_GUILD_ID}/scheduled-events", headers=headers)
    res_data = res.json()
    all_events = []

    for event in res_data:
        with engine.connect() as conn:
            result = conn.execute(text(
                '''
                SELECT record_id FROM discord_event_mappings
                WHERE event_id = '{event_id}'
                '''.format(event_id=event['id'])
            ))
            record_id = None
            for row in result:
                record_id = row.record_id

            all_events.append(
                DiscordEvent(
                    id=event['id'],
                    record_id=record_id,
                    name=event['name'],
                    description=event['description'],
                    start_time=event['scheduled_start_time'],
                    end_time=event['scheduled_end_time'],
                    status=DiscordEventStatus(event['status']),
                    metadata=DiscordEventMetadata(
                        location=event['entity_metadata']['location']
                    ),
                    image=event['image']
                )
            )

    return all_events


def create_event(
        record_id: str,
        name: str,
        description: str,
        start_time: str,
        end_time: str,
        location: str,
        image: str
):
    post_body = {
        'entity_metadata': {
            'location': location
        },
        'name': name,
        'privacy_level': 2,
        'scheduled_start_time': start_time,
        'scheduled_end_time': end_time,
        'description': description,
        'entity_type': 3,
        'image': image
    }
    headers = {
        'Authorization': f"Bot {DISCORD_TOKEN}"
    }
    res = requests.post(f"{BASE_URL}/guilds/{DISCORD_GUILD_ID}/scheduled-events", json=post_body, headers=headers)
    res_data = res.json()

    if "id" in res_data:
        with engine.connect() as conn:
            conn.execute(text(
                '''
                INSERT INTO discord_event_mappings (record_id, event_id)
                VALUES ('{record_id}', '{event_id}')
                '''.format(record_id=record_id, event_id=res_data['id'])
            ))

    return res_data


def get_event(record_id: str):
    headers = {
        'Authorization': f"Bot {DISCORD_TOKEN}"
    }
    with engine.connect() as conn:
        result = conn.execute(text(
            '''
            SELECT event_id FROM discord_event_mappings
            WHERE record_id = '{record_id}'
            '''.format(record_id=record_id)
        ))
        event_id = None
        for row in result:
            event_id = row.event_id

        if event_id is None:
            return None

    res = requests.get(f"{BASE_URL}/guilds/{DISCORD_GUILD_ID}/scheduled-events/{event_id}", headers=headers)
    res_data = res.json()

    return DiscordEvent(
        id=res_data['id'],
        record_id=record_id,
        name=res_data['name'],
        description=res_data['description'],
        start_time=res_data['scheduled_start_time'],
        end_time=res_data['scheduled_end_time'],
        status=DiscordEventStatus(res_data['status']),
        metadata=DiscordEventMetadata(
            location=res_data['entity_metadata']['location']
        ),
        image=res_data['image']
    )


def update_event(
        record_id: str,
        name: str,
        description: str,
        start_time: str,
        end_time: str,
        location: str,
        image: str,
):
    headers = {
        'Authorization': f"Bot {DISCORD_TOKEN}"
    }
    with engine.connect() as conn:
        result = conn.execute(text(
            '''
            SELECT event_id FROM discord_event_mappings
            WHERE record_id = '{record_id}'
            '''.format(record_id=record_id)
        ))
        event_id = None
        for row in result:
            event_id = row.event_id

        if event_id is None:
            return None

    post_body = {
        'entity_metadata': {
            'location': location
        },
        'name': name,
        'privacy_level': 2,
        'scheduled_start_time': start_time,
        'scheduled_end_time': end_time,
        'description': description,
        'entity_type': 3,
        'image': image
    }

    if description is None:
        del post_body['description']

    res = requests.patch(f"{BASE_URL}/guilds/{DISCORD_GUILD_ID}/scheduled-events/{event_id}", json=post_body, headers=headers)
    return res.json()


def delete_event(record_id: str):
    headers = {
        'Authorization': f"Bot {DISCORD_TOKEN}"
    }
    with engine.connect() as conn:
        result = conn.execute(text(
            '''
            SELECT event_id FROM discord_event_mappings
            WHERE record_id = '{record_id}'
            '''.format(record_id=record_id)
        ))
        event_id = None
        for row in result:
            event_id = row.event_id

        if event_id is None:
            return None

        conn.execute(text(
            '''
            DELETE FROM discord_event_mappings
            WHERE record_id = '{record_id}'
            '''.format(record_id=record_id)
        ))

    res = requests.delete(f"{BASE_URL}/guilds/{DISCORD_GUILD_ID}/scheduled-events/{event_id}", headers=headers)
    return res.text


