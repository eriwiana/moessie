from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Moessie"
    deta_project_key: str
    base_members_name: str
    base_subscriptions_name: str

    static_path: str = "/static"
    static_dir: str = "/static"
    static_name: str = "static"

    templates_dir: str = "/templates"

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings():
    return Settings()
