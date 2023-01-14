import json
from http import HTTPStatus
from typing import Optional

from fastapi.templating import Jinja2Templates

from base import settings


class BaseView:
    base = None
    templates = Jinja2Templates(directory=settings.templates_dir)
    list_templates = "list.html"

    def __init__(self):
        if not self.base:
            raise Exception("Base View `base` can not be empty!")

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
