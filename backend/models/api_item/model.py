from faker import Faker
from tortoise import fields

from backend.models.base import MyAbstractBaseModel, TimeDataMixin


class ApiItem(MyAbstractBaseModel, TimeDataMixin):
    label = fields.CharField(80, required=True)
    description = fields.TextField(required=True)
    url = fields.TextField(required=True)

    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
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
