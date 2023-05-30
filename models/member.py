from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class MemberCreate(BaseModel):
    name: str
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class MemberUpdate(BaseModel):
    name: str
    modified: datetime = Field(default_factory=datetime.now)


class MemberDetail(BaseModel):
    key: str
    name: str
    created: datetime
    modified: datetime
