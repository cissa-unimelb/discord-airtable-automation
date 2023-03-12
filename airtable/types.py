from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebhookSpecInclude:
    include_cell_values_in_field_ids: [str]
    include_previous_cell_values: bool


@dataclass
class WebhookSpecFilter:
    data_type: [str]
    record_change_scope: str
    watch_data_in_field_ids: [str]


@dataclass
class WebhookSpecification:
    filters: WebhookSpecFilter
    includes: WebhookSpecInclude


@dataclass
class Webhook:
    id: str
    cursor_for_next_payload: int
    is_hook_enabled: bool
    notification_url: str
    expiration_time: str
    specification: WebhookSpecification


@dataclass
class FieldValue:
    id: str
    curr: str
    prev: str = None


@dataclass
class Record:
    id: str
    name: str
    fields: [FieldValue]


@dataclass
class WebhookPayload:
    timestamp: datetime
    changed_records: [Record]
    created_records: [Record]


