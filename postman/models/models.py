from enum import Enum
from random import choice, randint, uniform

from faker import Faker
from tortoise import Tortoise, fields

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

    @classmethod
    def random_dict(cls, save=True):
        fake = Faker()

        data = {
            "name": fake.word(),
            "level": randint(0, 7),
            "description": fake.paragraph(),
        }

        return data


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

    @classmethod
    def random_dict(cls):
        fake = Faker()

        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "password": fake.password(),
            "active": choice([True, False]),
        }

        return data


class Tag(MyAbstractBaseModel):
    text = fields.CharField(50, unique=True)

    api_items: fields.ManyToManyRelation["ApiItem"]
    endpoints: fields.ManyToManyRelation["Endpoint"]

    def __str__(self):
        return self.text

    @classmethod
    def random_dict(cls):
        fake = Faker()

        data = {"text": fake.word()}

        return data


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

    @classmethod
    def random_dict(cls):
        fake = Faker()

        data = {
            "label": fake.word(),
            "description": fake.paragraph(),
            "url": fake.url(),
        }

        return data


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

    @classmethod
    def random_dict(cls):
        fake = Faker()

        data = {
            "url": fake.uri_path(),
            "label": fake.word(),
            "description": fake.paragraph(),
            "http_method": choice([m.value for m in HttpMethod]),
        }

        return data


class ParamLocation(str, Enum):
    HEADER = "header"
    PATH = "path"
    QUERY = "query"
    Body = "body"


class TypeParam(str, Enum):
    INTEGER = "integer"
    STRING = "string"
    FLOAT = "float"


class QueryParam(MyAbstractBaseModel, TimeDataMixin):
    label = fields.CharField(80, required=True)
    type = fields.CharEnumField(TypeParam, required=True)
    description = fields.TextField()
    default = fields.CharField(200, required=False, null=True)
    required = fields.BooleanField(default=False)
    location = fields.CharEnumField(ParamLocation, required=True)

    endpoint: fields.ForeignKeyRelation[Endpoint] = fields.ForeignKeyField(
        "models.Endpoint", related_name="query_params"
    )

    def __str__(self):
        return self.label

    @classmethod
    def random_dict(cls):
        fake = Faker()

        type_ = choice([pl.value for pl in TypeParam])
        if type_ == TypeParam.INTEGER:
            default = randint(0, 1000000)
        elif type_ == TypeParam.FLOAT:
            default = uniform(0, 10000)
        else:
            default = fake.word()

        data = {
            "label": fake.word(),
            "description": fake.paragraph(),
            "type": type_,
            "default": default,
            "required": choice([True, False]),
            "location": choice([pl.value for pl in ParamLocation]),
        }

        return data


settings = get_settings()
Tortoise.init_models(settings.TORTOISE_MODELS["models"], "models")
