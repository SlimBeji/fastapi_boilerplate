from fastapi import FastAPI

from postman.config import get_settings


def create_app():
    app = FastAPI()
    settings = get_settings()

    return app
