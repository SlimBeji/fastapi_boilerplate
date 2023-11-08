import os

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict

FILEDIR = os.path.dirname(__file__)


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ENV: str

    TORTOISE_MODELS: dict = {
        "models": ["backend.models", "aerich.models"],
    }
    TORTOISE_CONNECTION_NAME: str = "default"

    MAX_ITEM_PER_RESPONSE: int = 20

    FRONTEND_FOLDER: str = os.path.join(FILEDIR, os.pardir, "frontend")
    TEMPLATES_FOLDER: str = os.path.join(FRONTEND_FOLDER, "templates")
    STATIC_FOLDER: str = os.path.join(FRONTEND_FOLDER, "static")

    _CONFIG = SettingsConfigDict(env_file=os.path.join(FILEDIR, os.pardir, ".env"))


settings = Settings()
templates = Jinja2Templates(settings.TEMPLATES_FOLDER)
static_files = StaticFiles(directory=settings.STATIC_FOLDER)
aerich_config = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": settings.TORTOISE_MODELS["models"],
            "default_connection": settings.TORTOISE_CONNECTION_NAME,
        }
    },
}
