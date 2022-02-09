from tortoise import Tortoise

from postman.config import get_settings

from .models import ApiItem, Endpoint, QueryParam, Role, Tag, User


async def init_db():
    settings = get_settings()
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules=settings.TORTOISE_MODELS,
    )
    await Tortoise.generate_schemas()
