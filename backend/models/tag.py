from faker import Faker
from tortoise import fields

from backend.models.base import MyAbstractBaseModel


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
