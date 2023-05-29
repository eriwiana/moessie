from http import HTTPStatus

from fastapi import Request
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from base import deta
from base import settings
from base.messages import BaseMessage
from base.views import BaseView
from models.subscription import SubscriptionCreate
from models.subscription import SubscriptionDetail
from models.subscription import SubscriptionUpdate


router = InferringRouter()


@cbv(router)
class SubscriptionView(BaseView):
    base = deta.Base(settings.base_subscriptions_name)

    @router.get(
        "/api/subscription",
        response_model=list[SubscriptionDetail],
        responses={HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage}},
    )
    def get(
        self,
        request: Request,
        active: bool = True,
        limit: int = 10,
        last: str = None,
        order_by: str = "-key",
    ):
        """Subscription List API View"""

        query = {}
        if request.query_params:
            query = dict(request.query_params)
            query["active"] = active

        return self.list(
            request=request,
            query=query,
            limit=limit,
            last=last,
            order_by=order_by,
        )

    @router.get(
        "/api/subscription/{key}",
        response_model=SubscriptionDetail,
        responses={
            HTTPStatus.NOT_FOUND: {"model": BaseMessage},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def detail(self, key):
        """Subscription Detail API View"""

        return self.retrieve(key)

    @router.post(
        "/api/subscription",
        status_code=HTTPStatus.CREATED,
        response_model=SubscriptionDetail,
        responses={
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def post(self, data: SubscriptionCreate):
        """Subscription Create API View"""

        return self.create(data)

    @router.delete(
        "/api/subscription/{key}", status_code=HTTPStatus.NO_CONTENT
    )
    def delete(self, key: str):
        """Subscription Delete API View"""

        return self.base.delete(key)

    @router.patch(
        "/api/subscription/{key}",
        response_model=SubscriptionDetail,
        responses={
            HTTPStatus.NOT_FOUND: {"model": BaseMessage},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def patch(self, key: str, data: SubscriptionUpdate):
        """Subscription Update API View"""

        return self.update(key, data)
