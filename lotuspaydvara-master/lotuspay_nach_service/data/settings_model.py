from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class SettingsBase(BaseModel):
    number_of_sources_to_pick: int = 2
    number_of_iterations: int = 10
    # scheduler_start_in_seconds: int = 10
    # scheduler_end_in_seconds: int = 10
    created_date: datetime = Field(default_factory=datetime.now)


class SettingsCreate(BaseModel):
    number_of_sources_to_pick: int = 2
    number_of_iterations: int = 10
    # scheduler_start_in_seconds: int = 10
    # scheduler_end_in_seconds: int = 10


class SettingsDB(SettingsBase):
    id: int


settings_metadata = sqlalchemy.MetaData()


settings = sqlalchemy.Table(
    "settings",
    settings_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("number_of_sources_to_pick", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("number_of_iterations", sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column("scheduler_start_in_seconds", sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column("scheduler_end_in_seconds", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
)



