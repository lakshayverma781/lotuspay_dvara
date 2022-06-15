from datetime import datetime
from lib2to3.pgen2 import token
from typing import Optional


import sqlalchemy
from pydantic import BaseModel, Field

class PhyDB(BaseModel):
    id: int  


physical_mandates_metadata=sqlalchemy.MetaData()

physical = sqlalchemy.Table(
    "physical",
    physical_mandates_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("physical_id", sqlalchemy.String(length=255), nullable=True),

    sqlalchemy.Column("object", sqlalchemy.String(length=255), nullable=True),
    
    sqlalchemy.Column("created", sqlalchemy.String(length=255), nullable=True),
   
    sqlalchemy.Column("mandate", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("source", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("reference1", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True)
    
)