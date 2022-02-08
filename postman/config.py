import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")


@lru_cache()
def get_settings():
    return Settings()
