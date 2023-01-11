from http import HTTPStatus

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from base.collection import BaseCollection
from base.views import BaseTemplateView


router = InferringRouter()


@cbv(router)
class SubscriptionView(BaseTemplateView):
    base = BaseCollection("subscription")

    @router.get("/subscriptions", response_class=HTMLResponse)
    def get(self, request: Request):
        """Subscription List Template View"""

        return super(SubscriptionView, self).list(
            request=request, data=self.base.list()
        )

    @router.post("/api/subscription", status_code=HTTPStatus.CREATED)
    def post(self, body: dict):
        """Subscription API Create View"""

        return self.base.create(body)

    @router.delete(
        "/api/subscription/{key}", status_code=HTTPStatus.NO_CONTENT
    )
    def delete(self, key: str):
        """Subscription API Delete View"""

        return self.base.delete(key)

    @router.patch("/api/subscription/{key}")
    def patch(self, key: str, body: dict):
        """Subscription API Update View"""

        return self.base.patch(key, body)
