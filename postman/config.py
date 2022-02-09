import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")

    TORTOISE_MODELS: dict = {
        "models": ["postman.models"],
    }
    TORTOISE_CONNECTION_NAME: str = "default"


@lru_cache()
def get_settings():
    return Settings()
