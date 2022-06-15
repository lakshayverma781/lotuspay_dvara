from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class NachDebitBase(BaseModel):
    amount_maximum: Optional[int] = 10000
    debtor_agent_code: Optional[str] = 'ICIC'
    debtor_account_name: Optional[str] = 'DVARA'
    debtor_account_number: Optional[str] = '123456'
    debtor_account_type: Optional[str] = 'savings'
    frequency: Optional[str] = 'MNTH'
    reference1: Optional[str] = 'CU0056G1KRMKT3'


class SourceBase(BaseModel):
    source_id: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    type: Optional[str] = None
    nach_debit: NachDebitBase


class Source2Base(BaseModel):
    source_id: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    type: Optional[str] = None
    nach_debit: NachDebitBase
    redirect: Optional[str] = None
    customer: Optional[str] = None


class Source3Base(BaseModel):
    source_id: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    type: Optional[str] = None
    nach_debit: NachDebitBase
    redirect: Optional[str] = None
    bank_account: Optional[str] = None


class SourceRedirect(BaseModel):
    return_url: Optional[str] = 'https://www.lotuspay.com/'


class SourceCreate(BaseModel):
    type: Optional[str] = 'nach_debit'
    nach_debit: NachDebitBase


class Source2Create(BaseModel):
    type: Optional[str] = 'nach_debit'
    nach_debit: NachDebitBase
    redirect: SourceRedirect
    customer: Optional[str] = 'CU0011AABBCC22'


class Source3Create(BaseModel):
    type: Optional[str] = 'nach_debit'
    nach_debit: NachDebitBase
    redirect: SourceRedirect
    bank_account: Optional[str] = 'BA004433221AA'


class NachDebitBase5(BaseModel):
    amount_maximum: Optional[int] = 10000
    date_first_collection:Optional[str]='2020-01-01'
    debtor_account_name: Optional[str] = 'DVARA'
    debtor_account_number: Optional[str] = '123456'
    debtor_account_type: Optional[str] = 'savings'
    debtor_agent_mmbid: Optional[str]='ICIC0000001'
    debtor_email: Optional[str]='test@lotuspay.com'
    debtor_mobile: Optional[str]='9123456789'
    frequency: Optional[str] = 'MNTH'
    reference1: Optional[str] = 'LOAN_ID_123'
    variant: Optional[str]= "physical"


class Source5Create(BaseModel):
    type: Optional[str] = 'nach_debit'
    nach_debit: NachDebitBase5


class SourceDB(SourceBase):
    id: int


source_metadata = sqlalchemy.MetaData()


sources = sqlalchemy.Table(
    "sources",
    source_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("source_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("type", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("amount_maximum", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("date_first_collection", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_agent_code", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_account_name", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_account_number", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_account_type", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_agent_mmbid", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_email", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("debtor_mobile", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("frequency", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("reference1", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("variant", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("redirect", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("customer", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("bank_account", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("bank_account_token", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("source_status", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mandate_status", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)

perdix_metadata = sqlalchemy.MetaData()

perdix_customer = sqlalchemy.Table(
    "perdix_customer",
    perdix_metadata ,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("source_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mandate_url", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("source_status",sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("mandate_id",sqlalchemy.String(length=255),nullable=True),
    sqlalchemy.Column("mandate_status",sqlalchemy.String(length=255),nullable=True),
    sqlalchemy.Column("perdix_customer_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("perdix_enrollment_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("lotuspay_customer_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("bank_account", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("bank_account_token", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("iterations", sqlalchemy.Integer, default=0, nullable=True),
    sqlalchemy.Column("pending", sqlalchemy.Boolean, default=0, nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)