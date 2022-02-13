from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    TORTOISE_MODELS: dict = {
        "models": ["postman.models.models"],
    }
    TORTOISE_CONNECTION_NAME: str = "default"

    MAX_ITEM_PER_RESPONSE = 20

    class Config:
        env_file = "../.env"



@lru_cache()
def get_settings():
    return Settings()
