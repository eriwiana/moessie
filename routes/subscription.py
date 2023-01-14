from http import HTTPStatus

from fastapi import Request
from fastapi import Response
from fastapi.responses import HTMLResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from base import deta
from base import settings
from base.views import BaseView
from models.subscription import SubscriptionCreate
from models.subscription import SubscriptionUpdate


router = InferringRouter()


@cbv(router)
class SubscriptionView(BaseView):
    base = deta.Base(settings.base_subscriptions_name)

    @router.get("/subscriptions", response_class=HTMLResponse)
    def get(self, request: Request):
        """Subscription List Template View"""

        return self.list(request=request)

    @router.get("/api/subscription/{key}")
    def detail(self, key, response: Response):
        """Subscription Detail API View"""

        return self.retrieve(key, response)

    @router.post("/api/subscription", status_code=HTTPStatus.CREATED)
    def post(self, data: SubscriptionCreate, response: Response):
        """Subscription Create API View"""

        return self.create(data, response)

    @router.delete(
        "/api/subscription/{key}", status_code=HTTPStatus.NO_CONTENT
    )
    def delete(self, key: str):
        """Subscription Delete API View"""

        return self.base.delete(key)

    @router.patch("/api/subscription/{key}")
    def patch(self, key: str, data: SubscriptionUpdate, response: Response):
        """Subscription Update API View"""

        return self.update(key, data, response)
