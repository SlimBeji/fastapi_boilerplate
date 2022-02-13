# flake8: noqa
from tortoise import Tortoise

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
