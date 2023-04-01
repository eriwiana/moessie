import json
from collections import namedtuple
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi.templating import Jinja2Templates

from base import settings
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
    templates = Jinja2Templates(directory=settings.templates_dir)
    list_templates = "list.html"

    def __init__(self):
        if not self.base:
            raise Exception("Base View `base` can not be empty!")

        self.templates.env.filters["next_payment"] = next_payment
        self.templates.env.filters["format_currency"] = format_currency

    def list(
        self, request, query: Optional[dict] = None, order_by: str = "-key"
    ) -> Jinja2Templates.TemplateResponse:
        """Base List Template View"""

        data = sorted(
            self.base.fetch(query).items,
            key=lambda i: i.get(order_by.split("-")[1]),
            reverse="-" in order_by,
        )

        return self.templates.TemplateResponse(
            name=self.list_templates,
            context={"request": request, "data": data},
        )

    def retrieve(self, key, response) -> dict:
        try:
            data = self.base.get(key)

            if not data:
                response.status_code = HTTPStatus.NOT_FOUND
                return {"message": "Not found."}

            return data
        except Exception as err:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return {"message": str(err)}

    def create(self, data, response) -> dict:
        """Base Create API View"""

        try:
            return self.base.put(json.loads(data.json()))
        except Exception as err:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return {"message": str(err)}

    def update(self, key: str, data, response) -> dict:
        """Base Update API View"""

        try:
            self.base.update(json.loads(data.json(exclude_none=True)), key)
            return self.base.get(key)
        except Exception as err:
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

            # Set response status code if error key is not found.
            if "not found" in str(err):
                response.status_code = HTTPStatus.NOT_FOUND

            return {"message": str(err)}
