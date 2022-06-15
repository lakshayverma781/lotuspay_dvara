from datetime import datetime
from typing import Optional

import sqlalchemy


events_metadata = sqlalchemy.MetaData()


events = sqlalchemy.Table(
    "events",
    events_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("event_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_created", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_livemode", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column("resource_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_created", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_status", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
)

# {'id': 'EV0044332211AA', 'object': 'event', 'created': 1530224170, 'livemode': False, 'data': {'id': 'MD0044332211AA', 'object': 'mandate', 'created': 1530224170},
# 'type': 'mandate.active'}

{"serialized_response": "3a325657be9cb30fQUsr3Y8kBSiUyO/hj74Z5UNqxXE3h7vv0TW60Psg8rx53GFqlryO5nWtRalr\n/nN2jx17prY/Hy4vcBqpsDs0Gw9z6hL0OYGH2IDLRAdz9EBzfHluV1BKYqz6\n1tgY7Sou306FFIqUoVmmXbpcHo4ctW0VqJPOBlWItUneeMCt4JpJPZ80pHNr\nrxOVPzFexuXe7rYIu8TrMGU+sRmsvINmsc+J9idmcNFcpjg4njZ0jH8=\n"}