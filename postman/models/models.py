from tortoise import fields

from .mixins import MyModel, PrimaryKey, TimeData


class Role(MyModel, PrimaryKey):
    name = fields.CharField(255, unique=True)
    level = fields.IntField()
    description = fields.TextField()

    users: fields.ReverseRelation["User"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(MyModel, PrimaryKey):
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


class Tag(MyModel, PrimaryKey):
    text = fields.CharField(50, unique=True)

    api_items: fields.ManyToManyRelation["ApiItem"]
    api_items: fields.ManyToManyRelation["Endpoint"]

    def __str__(self):
        return self.text


class ApiItem(MyModel, PrimaryKey, TimeData):
    label = fields.CharField(80, required=True)
    description = fields.TextField(required=True)
    url = fields.TextField(required=True)

    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="apis", through="tag_api"
    )

    endpoints: fields.ReverseRelation["Endpoint"]

    def __str__(self):
        return self.url


class Endpoint(MyModel, PrimaryKey, TimeData):
    url = fields.TextField(required=True)
    label = fields.CharField(80)
    description = fields.TextField()
    http_method = fields.CharField(10, required=True)

    api_item: fields.ForeignKeyRelation[ApiItem] = fields.ForeignKeyField(
        "models.ApiItem", related_name="endpoints"
    )

    query_params = fields.ReverseRelation["QueryParam"]

    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="endpoints", through="tag_endpoint"
    )

    def __str__(self):
        return self.url


class QueryParam(MyModel, PrimaryKey, TimeData):
    label = fields.CharField(80, required=True)
    type = fields.CharField(20, required=True)
    description = fields.TextField()
    default = fields.CharField(200, required=False, null=True)
    required = fields.BooleanField(default=False)
    location = fields.CharField(20, required=True)

    endpoint: fields.ForeignKeyRelation[Endpoint] = fields.ForeignKeyField(
        "models.Endpoint", related_name="query_params"
    )

    def __str__(self):
        return self.label
