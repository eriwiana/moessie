from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from base import settings
from routes.member import router as member_router
from routes.subscription import router as subscription_router


app = FastAPI(
    title=settings.app_name, docs_url=None, openapi_url=None, redoc_url=None
)

# Serve Static files
app.mount(
    settings.static_path,
    StaticFiles(directory=settings.static_dir),
    name=settings.static_name,
)

app.include_router(subscription_router)
app.include_router(member_router)
