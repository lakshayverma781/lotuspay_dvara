from datetime import datetime
from typing import Optional
import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy.dialects.mysql import LONGTEXT


class MandateBase(BaseModel):
    mandate_id: Optional[str] = None
    token: Optional[str] = None
    metadata: str
    created_date: datetime = Field(default_factory=datetime.now)


class MandateCancelCreate(BaseModel):
    cancel_reason: Optional[str] = None


class MandateImportCreate(BaseModel):
    amount_collection: Optional[int] = 10000
    category_code:Optional[str]='L001'
    category_description: Optional[str] = 'DVARA'
    creditor_agent_mmbid: Optional[str] = '123456'
    creditor_name: Optional[str] = 'savings'
    creditor_utility_code: Optional[str]='ICIC0000001'
    date_first_collection: Optional[str]='test@lotuspay.com'
    debtor_account_name: Optional[str]='9123456789'
    debtor_account_number: Optional[str] = '123456'
    debtor_account_type: Optional[str] = 'savings'
    debtor_agent_mmbid: Optional[str]='ICIC0000001'
    instrument: Optional[str]="DEBIT"
    occurrence_sequence_type: Optional[str]="RCUR"
    reference1:Optional[str]= "CU0029P5MX9CZF"
    umrn: Optional[str]="ICIC0000000000272000"
    date_acknowledged: Optional[str]="2020-01-01"
    date_responded:Optional[str]= "2020-01-05"
    mandate_request_id: Optional[str]="MD0062TFGVUPSZ"


class MandateDB(MandateBase):
    id: int


mandate_metadata = sqlalchemy.MetaData()


mandates = sqlalchemy.Table(
    "mandates",
    mandate_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("metadata", sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)


mandates_cancel = sqlalchemy.Table(
    "mandates_cancel",
    mandate_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)


mandates_import_external = sqlalchemy.Table(
    "mandates_import_external",
    mandate_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
)