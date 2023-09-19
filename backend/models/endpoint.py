from random import choice

from faker import Faker
from tortoise import fields

from backend.enums.http import HttpMethod
from backend.models.base import MyAbstractBaseModel, TimeDataMixin


class Endpoint(MyAbstractBaseModel, TimeDataMixin):
    url = fields.TextField(required=True)
    label = fields.CharField(80)
    description = fields.TextField()
    http_method = fields.CharEnumField(
        HttpMethod, required=True, default=HttpMethod.GET
    )

    api_item: fields.ForeignKeyRelation["ApiItem"] = fields.ForeignKeyField(
        "models.ApiItem", related_name="endpoints"
    )

    query_params = fields.ReverseRelation["QueryParam"]

    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
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
