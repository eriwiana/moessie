import os
from typing import Optional

from deta import Deta

deta = Deta(os.getenv("DETA_PROJECT_KEY"))


class BaseCollection:
    def __init__(self, name):
        self.base = deta.Base(name)

    def create(self, body: dict):
        return self.base.put(body)

    def list(self, query: Optional[dict] = None, order_by: str = "-key"):
        return sorted(
            self.base.fetch(query).items,
            key=lambda i: i.get(order_by.split("-")[1]),
            reverse="-" in order_by,
        )

    def retrieve(self, key: str):
        return self.base.get(key)

    def patch(self, key: str, body: dict):
        try:
            return self.base.update(body, key)
        except Exception as err:
            return {"message": str(err)}

    def delete(self, key: str):
        return self.base.delete(key)
