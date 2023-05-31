from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class BillingEnum(str, Enum):
    monthly = "monthly"
    annually = "annually"


class SubscriptionCreate(BaseModel):
    name: str
    price: float = Field(default=0.0, ge=0.0)
    billing: BillingEnum = BillingEnum.monthly
    active: bool = Field(default=True)
    renewal_date: datetime = Field(default_factory=datetime.now)
    last_subscribed_date: datetime = Field(default=None)
    member_limit: int = Field(default=1, le=6)
    members: List[str] = Field(default=[], min_items=0, max_items=6)
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None, ge=0.0)
    billing: Optional[BillingEnum] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    renewal_date: Optional[datetime] = Field(default=None)
    last_subscribed_date: Optional[datetime] = Field(default=None)
    member_limit: Optional[int] = Field(default=None, le=6)
    members: Optional[List[str]] = Field(default=[], min_items=0, max_items=6)
    modified: datetime = Field(default_factory=datetime.now)


class SubscriptionDetail(BaseModel):
    key: str
    name: str
    price: float
    billing: BillingEnum
    active: bool
    renewal_date: datetime
    last_subscribed_date: Optional[datetime]
    member_limit: int
    members: Optional[List[str]]
    created: datetime
    modified: datetime


class SubscriptionMemberCreate(BaseModel):
    members: List[str] = Field(default=[], min_items=0, max_items=6)
