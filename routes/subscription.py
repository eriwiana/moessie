from http import HTTPStatus

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from base import deta
from base import settings
from base import views
from base.messages import BaseMessage
from base.views import BaseView
from models.subscription import SubscriptionCreate
from models.subscription import SubscriptionDetail
from models.subscription import SubscriptionMemberCreate
from models.subscription import SubscriptionUpdate


router = InferringRouter()


@cbv(router)
class SubscriptionView(BaseView):
    base = deta.Base(settings.base_subscriptions_name)
    templates = Jinja2Templates(directory="dashboard/templates")
    templates.env.filters["next_payment"] = views.next_payment
    templates.env.filters["format_currency"] = views.format_currency

    @router.get("/", response_class=HTMLResponse)
    def home(self, request: Request):
        data = self.get(request)

        for d in data:
            members = d.get("members", [])
            if members:
                member_base = deta.Base(settings.base_members_name)
                _members = []
                for k in members:
                    member = member_base.get(k)
                    _members.append(member.get("name"))
                d["members"] = _members

        return self.templates.TemplateResponse(
            name="list.html", context={"request": request, "data": data}
        )

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

    @router.patch(
        "/api/subscription/{key}/members",
        response_model=SubscriptionDetail,
        responses={
            HTTPStatus.NOT_FOUND: {"model": BaseMessage},
            HTTPStatus.BAD_REQUEST: {"model": BaseMessage},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def update_member(self, key: str, data: SubscriptionMemberCreate):
        """Update Subscription's Member API View"""

        subscription_data = self.retrieve(key)
        if isinstance(subscription_data, JSONResponse):
            return subscription_data

        # Validate member limit
        member_limit = subscription_data.get("member_limit")
        if len(data.members) > member_limit:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={
                    "message": f"Member Limit is {member_limit} account(s)."
                },
            )

        return self.update(key, data)
