from http import HTTPStatus

from fastapi import Request
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from base import deta
from base import settings
from base.messages import BaseMessage
from base.views import BaseView
from models.member import MemberCreate
from models.member import MemberDetail
from models.member import MemberUpdate


router = InferringRouter()


@cbv(router)
class MemberView(BaseView):
    base = deta.Base(settings.base_members_name)

    @router.get(
        "/api/member",
        response_model=list[MemberDetail],
        responses={HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage}},
    )
    def get(
        self,
        request: Request,
        limit: int = 10,
        last: str = None,
        order_by: str = "-key",
    ):
        """Member List API View"""

        query = {}
        if request.query_params:
            query = dict(request.query_params)

        return self.list(
            request=request,
            query=query,
            limit=limit,
            last=last,
            order_by=order_by,
        )

    @router.get(
        "/api/member/{key}",
        response_model=MemberDetail,
        responses={
            HTTPStatus.NOT_FOUND: {"model": BaseMessage},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def detail(self, key):
        """Member Detail API View"""

        return self.retrieve(key)

    @router.post(
        "/api/member",
        status_code=HTTPStatus.CREATED,
        response_model=MemberDetail,
        responses={
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def post(self, data: MemberCreate):
        """Member Create API View"""

        return self.create(data)

    @router.delete("/api/member/{key}", status_code=HTTPStatus.NO_CONTENT)
    def delete(self, key: str):
        """Member Delete API View"""

        return self.base.delete(key)

    @router.patch(
        "/api/member/{key}",
        response_model=MemberDetail,
        responses={
            HTTPStatus.NOT_FOUND: {"model": BaseMessage},
            HTTPStatus.INTERNAL_SERVER_ERROR: {"model": BaseMessage},
        },
    )
    def patch(self, key: str, data: MemberUpdate):
        """Member Update API View"""

        return self.update(key, data)
