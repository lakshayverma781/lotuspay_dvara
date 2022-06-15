from datetime import datetime
from lib2to3.pgen2 import token
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field




class BankAccount(BaseModel):
    account_holder_name: Optional[str] = "AMIT JAIN"
    account_ifsc:Optional[str]='ICIC0000043'
    account_number: Optional[str] = '12345678'
    account_type: Optional[str] = 'savings'

class BankAccount2(BaseModel):  
    account_holder_name: Optional[str] = "AMIT JAIN"
    account_ifsc:Optional[str]='ICIC0000043'
    account_number: Optional[str] = '12345678'  

class TokenBase (BaseModel):
    token_id: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    bank_account: BankAccount

class TokenCreate(BaseModel):
    bank_account:BankAccount

class TokenCreate2(BaseModel):
        bank_account:BankAccount2

class TokenDB(TokenBase):
    id: int    

token_metadata=sqlalchemy.MetaData()

tokens = sqlalchemy.Table(
    "tokens",
    token_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("token_id", sqlalchemy.String(length=255), nullable=True),
    
    
   
    sqlalchemy.Column("account_holder_name", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_number", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_type", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("account_ifsc", sqlalchemy.String(length=255), nullable=True),
    
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
    
)
   
