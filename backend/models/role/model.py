from random import randint

from faker import Faker
from tortoise import fields

from backend.models.base import MyAbstractBaseModel


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
    def random_dict(cls):
        fake = Faker()

        data = {
            "name": fake.word(),
            "level": randint(0, 7),
            "description": fake.paragraph(),
        }

        return data
