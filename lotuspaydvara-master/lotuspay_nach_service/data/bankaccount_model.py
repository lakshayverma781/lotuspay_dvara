from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class BankAccountBase(BaseModel):
    bank_account_id: Optional[str] = None
    customer_id: Optional[str] = None
    account_holder_name: Optional[str] = None
    account_ifsc: Optional[str] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)


class BankAccountCreate(BaseModel):
    account_holder_name: Optional[str] = 'Aroha Tech'
    account_ifsc: Optional[str] = 'ICIC0000047'
    account_number: Optional[str] = '12341234'
    account_type: Optional[str] = 'savings'
    customer_id: Optional[str] = None


class BankAccountDB(BankAccountBase):
    id: int


bankaccount_metadata = sqlalchemy.MetaData()


bankaccounts = sqlalchemy.Table(
    "bankaccounts",
    bankaccount_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("bank_account_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("customer_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_holder_name", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_ifsc", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_number", sqlalchemy.String(length=255), unique=True, nullable=True),
    sqlalchemy.Column("account_type", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)