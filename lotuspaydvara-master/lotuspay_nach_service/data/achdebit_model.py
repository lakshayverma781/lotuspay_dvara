from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class ACHDebitBase(BaseModel):
    achdebit_id: Optional[str] = None
    amount: Optional[int] = 10000
    mandate: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)


class ACHDebitCreate(BaseModel):
    amount: Optional[int] = 10000
    mandate: Optional[str] = 'MD0055BQXKA2DG'


class ACHDebitDB(ACHDebitBase):
    id: int


achdebit_metadata = sqlalchemy.MetaData()


achdebits = sqlalchemy.Table(
    "achdebits",
    achdebit_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("achdebit_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("mandate", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)

achdebits_cancel = sqlalchemy.Table(
    "achdebits_cancel",
    achdebit_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("achdebit_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)