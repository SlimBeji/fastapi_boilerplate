# flake8: noqa
from tortoise import Tortoise

from postman.config import get_settings

from .models import (
    ApiItem,
    Endpoint,
    HttpMethod,
    ParamLocation,
    QueryParam,
    Role,
    Tag,
    User,
)

Tortoise.init_models(["postman.models"], "models")


async def init_db():
    settings = get_settings()
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules=settings.TORTOISE_MODELS,
    )
    await Tortoise.generate_schemas()
