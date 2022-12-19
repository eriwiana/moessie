from http import HTTPStatus

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from base.collection import BaseCollection


router = InferringRouter()


@cbv(router)
class SubscriptionView:
    base = BaseCollection("subscription")

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
