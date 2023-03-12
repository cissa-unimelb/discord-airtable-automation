from airtable.types import *

NAME_FIELD_ID = 'fldndprPs52tyQ35m'


def collect_fields(arg):
    record_id, val = arg
    fields = []
    name = None

    if 'current' in val:
        val_cur = val['current']
    else:
        val_cur = val

    for field_id, field_val in val_cur['cellValuesByFieldId'].items():
        if field_id == NAME_FIELD_ID:
            name = field_val
        fields.append(FieldValue(id=field_id, curr=field_val))

    if 'previous' in val:
        for field_id, field_val in val['previous']['cellValuesByFieldId'].items():
            obj = next(x for x in fields if x.id == field_id)
            obj.prev = field_val

    if 'unchanged' in val:
        if name is None:
            name = val['unchanged']['cellValuesByFieldId'][NAME_FIELD_ID]
        for field_id, field_val in val['unchanged']['cellValuesByFieldId'].items():
            fields.append(FieldValue(id=field_id, curr=field_val))

    return Record(id=record_id, name=name, fields=fields)


def prune(payload_list):
    for i in range(0, len(payload_list) - 1):
        prev_payload: WebhookPayload = payload_list[i]
        for k in range(i + 1, len(payload_list)):
            curr_payload: WebhookPayload = payload_list[k]
            if curr_payload.changed_records is None or prev_payload.changed_records is None:
                continue

            time_diff = curr_payload.timestamp - prev_payload.timestamp

            if time_diff.total_seconds() < 10:
                for record in curr_payload.changed_records:
                    if any(x.id == record.id for x in prev_payload.changed_records):
                        prev_record: Record = next(x for x in prev_payload.changed_records if x.id == record.id)

                        for j in range(len(record.fields)):
                            field: FieldValue = record.fields[j]
                            if any(x.id == field.id for x in prev_record.fields):
                                prev_field = next(x for x in prev_record.fields if x.id == field.id)
                                prev_record.fields.remove(prev_field)
                                j -= 1

    for payload in payload_list:
        payload.changed_records = list(filter(lambda x: len(x.fields) != 0, payload.changed_records)) if payload.changed_records is not None else None
        payload.created_records = list(filter(lambda x: len(x.fields) != 0, payload.created_records)) if payload.created_records is not None else None

    return list(filter(lambda x: not ((x.changed_records is None or len(x.changed_records) == 0) and (x.created_records is None or len(x.created_records) == 0)), payload_list))
