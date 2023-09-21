from random import choice

from faker import Faker
from tortoise import fields

from backend.models.base import MyAbstractBaseModel, PasswordMixin, TimeDataMixin


class User(MyAbstractBaseModel, PasswordMixin, TimeDataMixin):
    first_name = fields.CharField(255)
    last_name = fields.CharField(255)
    email = fields.CharField(255)
    active = fields.BooleanField(default=False)

    role: fields.ForeignKeyNullableRelation["Role"] = fields.ForeignKeyField(
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
