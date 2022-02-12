from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from postman.api import api_routes
from postman.config import get_settings


def register_routers(app, routers):
    for router in routers:
        app.include_router(router)


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

    register_routers(app, api_routes)

    return app
