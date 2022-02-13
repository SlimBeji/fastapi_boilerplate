from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from postman.api import api_routes
from postman.config import settings, static_files
from postman.views import views_routes


def register_routers(app, routers):
    for router in routers:
        app.include_router(router)


def register_static_folder(
    app, static_files, name="static", endpoint="/static"
):
    app.mount(endpoint, static_files, name)


def create_app():
    app = FastAPI()

    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules=settings.TORTOISE_MODELS,
        generate_schemas=False,
        add_exception_handlers=True,
    )

    register_routers(app, api_routes)
    register_routers(app, views_routes)
    register_static_folder(app, static_files)

    return app
