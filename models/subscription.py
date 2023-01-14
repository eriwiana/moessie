from datetime import datetime
from enum import Enum
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
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None, ge=0.0)
    billing: Optional[BillingEnum] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    renewal_date: Optional[datetime] = Field(default=None)
    modified: datetime = Field(default_factory=datetime.now)
