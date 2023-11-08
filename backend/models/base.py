from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model


class TimeDataMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True)


class PasswordMixin:
    password = fields.CharField(255)

    @classmethod
    async def secure_create(cls, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = bcrypt.hash(kwargs["password"])

        return super().create(**kwargs)

    async def secure_update(self, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = bcrypt.hash(kwargs["password"])

        return super().update(**kwargs)

    def verify_password(self, plain_password):
        return bcrypt.verify(plain_password, self.password)


class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    @classmethod
    async def get_by_id(cls, id):
        item = await cls.get(id=id)
        return item

    @classmethod
    def search(cls, prefetch=None, first=False, distinct=True, **filters):
        query = cls.filter(**filters).order_by("id")
        if prefetch:
            query = query.prefetch_related(*prefetch)

        if distinct:
            query = query.distinct()

        if first:
            query = query.first()

        return query

    @classmethod
    def create_from_schema(cls, schema):
        return cls.create(**schema.dict(exclude_unset=True))

    async def update_from_schema(self, schema):
        record = self.update_from_dict(schema.dict(exclude_unset=True))
        await record.save()
        return record

    @classmethod
    def random_dict(cls, *args, **kwargs):
        """Used to easily create fake data in development"""
        raise NotImplementedError(
            f"{cls.__name__} did not implement random_dict method"
        )

    @classmethod
    def random(cls, *args, **kwargs):
        data = cls.random_dict(*args, **kwargs)
        record = cls(**data)
        return record

    @classmethod
    async def create_random(cls, *args, save=True, **kwargs):
        record = cls.random(*args, **kwargs)
        if save:
            await record.save()

        return record

    class Meta:
        abstract = True
