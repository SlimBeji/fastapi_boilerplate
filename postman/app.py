from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from postman.config import get_settings


def create_app():
    app = FastAPI()
    settings = get_settings()

    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules=settings.TORTOISE_MODELS,
        generate_schemas=False,
        add_exception_handlers=True,
    )

    return app
