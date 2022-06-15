from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    customer_id: Optional[str] = None
    email: str
    mobile: str
    name: str
    pan: str
    created_date: datetime = Field(default_factory=datetime.now)


class CustomerCreate(BaseModel):
    email: str = 'dvara1@dvara.com'
    mobile: str = '1234567890'
    name: str = 'DVARA1'
    pan: str = 'DVARA1'


class CustomerDB(CustomerBase):
    id: int


customer_metadata = sqlalchemy.MetaData()


customers = sqlalchemy.Table(
    "customers",
    customer_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("customer_id", sqlalchemy.String(length=255), unique=True, nullable=True),
    sqlalchemy.Column("email", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mobile", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("pan", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
)



