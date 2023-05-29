import json
from collections import namedtuple
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi.responses import JSONResponse

from models.subscription import BillingEnum


def next_payment(values):
    SUBSCRIPTION = namedtuple("Subscription", (k for k in values.keys()))
    data = SUBSCRIPTION(**values)

    dt = datetime.now()
    renewal_date = datetime.strptime(data.renewal_date, "%Y-%m-%dT%H:%M:%S")

    _month = dt.month if renewal_date.day >= dt.day else dt.month + 1

    if data.billing == BillingEnum.monthly:
        return datetime(dt.year, _month, renewal_date.day).strftime(
            "%B %d, %Y"
        )

    _year = (
        dt.year
        if renewal_date.day >= dt.day and renewal_date.month <= dt.month
        else dt.year + 1
    )
    return datetime(_year, _month, renewal_date.day).strftime("%B %d, %Y")


def format_currency(value):
    return f"{value:,}"


class BaseView:
    base = None

    def __init__(self):
        if not self.base:
            raise Exception("Base View `base` can not be empty!")

    def list(
        self,
        request,
        query: Optional[dict] = None,
        limit: int = 10,
        last: str = None,
        order_by: str = "-key",
    ) -> list[dict]:
        """Base List API View"""

        try:
            # Remove unnecessary attributes in query
            for k in ["limit", "last", "order_by"]:
                if k in query:
                    del query[k]

            return sorted(
                self.base.fetch(query=query, limit=limit, last=last).items,
                key=lambda i: i.get(order_by.replace("-", "")),
                reverse="-" in order_by,
            )
        except Exception as err:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": str(err)},
            )

    def retrieve(self, key) -> dict:
        """Base Detail API View"""

        try:
            data = self.base.get(key)

            if not data:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "Not found."},
                )
            return data
        except Exception as err:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": str(err)},
            )

    def create(self, data) -> dict:
        """Base Create API View"""

        try:
            return self.base.put(json.loads(data.json()))
        except Exception as err:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": str(err)},
            )

    def update(self, key: str, data) -> dict:
        """Base Update API View"""

        try:
            self.base.update(json.loads(data.json(exclude_none=True)), key)
            return self.base.get(key)
        except Exception as err:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

            # Set response status code if error key is not found.
            if "not found" in str(err):
                status_code = HTTPStatus.NOT_FOUND

            return JSONResponse(
                status_code=status_code, content={"message": str(err)}
            )
