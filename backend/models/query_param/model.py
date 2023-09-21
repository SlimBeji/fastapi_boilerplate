from random import choice, randint, uniform

from faker import Faker
from tortoise import fields

from backend.enums.http import ParamLocation, TypeParam
from backend.models.base import MyAbstractBaseModel, TimeDataMixin


class QueryParam(MyAbstractBaseModel, TimeDataMixin):
    label = fields.CharField(80, required=True)
    type = fields.CharEnumField(TypeParam, required=True)
    description = fields.TextField()
    default = fields.CharField(200, required=False, null=True)
    required = fields.BooleanField(default=False)
    location = fields.CharEnumField(ParamLocation, required=True)

    endpoint: fields.ForeignKeyRelation["Endpoint"] = fields.ForeignKeyField(
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
            "required": fake.boolean(),
            "location": choice([pl.value for pl in ParamLocation]),
        }

        return data
