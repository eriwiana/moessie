from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.subscription import router as subscription_router

app = FastAPI(title="Moessie", docs_url=None, openapi_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

app.include_router(subscription_router)
