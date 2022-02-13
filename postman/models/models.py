from enum import Enum

from tortoise import fields

from postman.config import get_settings

from .mixins import MyAbstractBaseModel, TimeDataMixin


class Role(MyAbstractBaseModel):
    name = fields.CharField(255, unique=True)
    level = fields.IntField()
    description = fields.TextField()

    users: fields.ReverseRelation["User"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(MyAbstractBaseModel):
    first_name = fields.CharField(255)
    last_name = fields.CharField(255)
    email = fields.CharField(255)
    password = fields.CharField(255)
    active = fields.BooleanField(default=False)

    role: fields.ForeignKeyNullableRelation[Role] = fields.ForeignKeyField(
        "models.Role", related_name="users"
    )

    def __str__(self):
        return self.email


class Tag(MyAbstractBaseModel):
    text = fields.CharField(50, unique=True)

    api_items: fields.ManyToManyRelation["ApiItem"]
    endpoints: fields.ManyToManyRelation["Endpoint"]

    def __str__(self):
        return self.text


class ApiItem(MyAbstractBaseModel, TimeDataMixin):
    label = fields.CharField(80, required=True)
    description = fields.TextField(required=True)
    url = fields.TextField(required=True)

    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="api_items", through="tag_apiitem"
    )

    endpoints: fields.ReverseRelation["Endpoint"]

    def __str__(self):
        return self.url


class HttpMethod(str, Enum):
    GET = "get"
    POST = "post"
    patch = "patch"
    put = "push"


class Endpoint(MyAbstractBaseModel, TimeDataMixin):
    url = fields.TextField(required=True)
    label = fields.CharField(80)
    description = fields.TextField()
    http_method = fields.CharEnumField(
        HttpMethod, required=True, default=HttpMethod.GET
    )

    api_item: fields.ForeignKeyRelation[ApiItem] = fields.ForeignKeyField(
        "models.ApiItem", related_name="endpoints"
    )

    query_params = fields.ReverseRelation["QueryParam"]

    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="endpoints", through="tag_endpoint"
    )

    def __str__(self):
        return self.url


class ParamLocation(str, Enum):
    HEADER = "header"
    PATH = "path"
    QUERY = "query"
    Body = "body"


class QueryParam(MyAbstractBaseModel, TimeDataMixin):
    label = fields.CharField(80, required=True)
    type = fields.CharField(20, required=True)
    description = fields.TextField()
    default = fields.CharField(200, required=False, null=True)
    required = fields.BooleanField(default=False)
    location = fields.CharEnumField(ParamLocation, required=True)

    endpoint: fields.ForeignKeyRelation[Endpoint] = fields.ForeignKeyField(
        "models.Endpoint", related_name="query_params"
    )

    def __str__(self):
        return self.label


settings = get_settings()
Tortoise.init_models(settings.TORTOISE_MODELS["models"], "models")
