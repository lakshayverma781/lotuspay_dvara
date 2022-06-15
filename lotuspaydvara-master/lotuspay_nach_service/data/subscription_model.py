from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class SubscriptionBase(BaseModel):
    subscription_id: Optional[str] = None
    amount: Optional[int] = 10000
    count: Optional[int] = 2
    day_of_month: Optional[int] = 6
    interval: Optional[str] = 'month'
    mandate: Optional[str] = 'MD0011DD22RR33'
    name: Optional[str] = 'Order 123'
    start_date: Optional[str] = '2022-04-01'
    created_date: datetime = Field(default_factory=datetime.now)


class SubscriptionCreate(BaseModel):
    amount: Optional[int] = 10000
    count: Optional[int] = 2
    day_of_month: Optional[int] = 6
    interval: Optional[str] = 'month'
    mandate: Optional[str] = 'MD0011DD22RR33'
    name: Optional[str] = 'Order 123'
    start_date: Optional[str] = '2022-04-01'


class SubscriptionDB(SubscriptionBase):
    id: int


subscription_metadata = sqlalchemy.MetaData()


subscriptions = sqlalchemy.Table(
    "subscriptions",
    subscription_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("subscription_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("count", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("day_of_month", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("interval", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mandate", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("start_date", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)


subscriptions_cancel = sqlalchemy.Table(
    "subscriptions_cancel",
    subscription_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("subscription_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)