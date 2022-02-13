import os
from functools import lru_cache

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

FILEDIR = os.path.dirname(__file__)


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    TORTOISE_MODELS: dict = {
        "models": ["postman.models.models"],
    }
    TORTOISE_CONNECTION_NAME: str = "default"

    MAX_ITEM_PER_RESPONSE = 20

    TEMPLATES_FOLDER = os.path.join(FILEDIR, "templates")
    STATIC_FOLDER = os.path.join(FILEDIR, "static")

    class Config:
        env_file = os.path.join(FILEDIR, os.pardir, ".env")


settings = Settings()
templates = Jinja2Templates(settings.TEMPLATES_FOLDER)
static_files = StaticFiles(directory=settings.STATIC_FOLDER)


@lru_cache()
def get_settings():
    return Settings()
