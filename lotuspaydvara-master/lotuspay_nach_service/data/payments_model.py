from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class PaymentBase(BaseModel):
    payment_id: Optional[str] = None
    amount: Optional[int] = 10000
    mandate: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)


class PaymentCreate(BaseModel):
    amount: Optional[int] = 10000
    mandate: Optional[str] = 'MD0055BQXKA2DG'


class PaymentDB(PaymentBase):
    id: int


payment_metadata = sqlalchemy.MetaData()


payments = sqlalchemy.Table(
    "payments",
    payment_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("payment_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("mandate", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
    # sqlalchemy.Column("created_date_time",sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)


payments_cancel = sqlalchemy.Table(
    "payments_cancel",
    payment_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("payment_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
    # sqlalchemy.Column("created_date_time",sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)