from tortoise import Tortoise

from backend.config import settings
from backend.models.api_item.model import ApiItem
from backend.models.endpoint.model import Endpoint
from backend.models.query_param.model import QueryParam
from backend.models.role.model import Role
from backend.models.tag.model import Tag
from backend.models.user.model import User

Tortoise.init_models(settings.TORTOISE_MODELS["models"], "models")
