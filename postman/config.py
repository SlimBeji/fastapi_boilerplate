import os
from functools import lru_cache

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

    class Config:
        env_file = os.path.join(FILEDIR, os.pardir, ".env")


settings = Settings()


@lru_cache()
def get_settings():
    return Settings()
