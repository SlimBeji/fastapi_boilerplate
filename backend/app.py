from typing import List, Optional

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from backend.api import api_routers
from backend.config import static_files
from backend.views import views_routers
from backend.config import settings


def register_routers(app: FastAPI, routers: List[APIRouter]):
    for router in routers:
        app.include_router(router)


def register_static_folder(
    app: FastAPI,
    static_files: StaticFiles,
    name: Optional[str] = "static",
    endpoint: Optional[str] = "/static",
):
    app.mount(endpoint, static_files, name)


def create_app() -> FastAPI:
    app = FastAPI()

    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules=settings.TORTOISE_MODELS,
    )
    register_routers(app, api_routers)
    register_routers(app, views_routers)
    register_static_folder(app, static_files)

    return app
