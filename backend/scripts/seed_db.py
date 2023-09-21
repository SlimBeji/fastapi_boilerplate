import json
import os

from tortoise import Tortoise, run_async

from backend.config import settings
from backend.enums.roles import SuperUser
from backend.models import ApiItem, Endpoint, QueryParam, Role, Tag, User

DIR_NAME = os.path.dirname(__file__)
JSON_DATA_PATH = os.path.join(DIR_NAME, "examples.json")


async def create_users(users):
    superuser_role = await Role.create(
        name=SuperUser.NAME,
        level=int(SuperUser.LEVEL),
        description=SuperUser.DESCRIPTION,
    )

    for user_data in users:
        user_role = user_data.pop("role")
        if user_role == SuperUser.NAME:
            await User.create(**user_data, role=superuser_role)


async def create_tags(tags):
    for text in tags:
        await Tag.create(text=text)


async def create_apis(api_list):
    for data in api_list:
        tags = data.pop("tags")
        endpoints = data.pop("endpoints")
        api_item = await ApiItem.create(**data)

        tag_instnaces = []
        for tag in tags:
            tag_instance = await Tag.get(text=tag)
            tag_instnaces.append(tag_instance)
        await api_item.tags.add(*tag_instnaces)

        for endpoint_data in endpoints:
            endpoint_tags = endpoint_data.pop("tags")
            query_params = endpoint_data.pop("query_params")
            endpoint_item = await Endpoint.create(**endpoint_data, api_item=api_item)

            endpoint_tag_instnaces = []
            for tag in endpoint_tags:
                tag_instance = await Tag.get(text=tag)
                endpoint_tag_instnaces.append(tag_instance)
            await endpoint_item.tags.add(*endpoint_tag_instnaces)

            for query_param_data in query_params:
                await QueryParam.create(**query_param_data, endpoint=endpoint_item)


async def seed_db():
    # Initializing Tortoise-ORM
    await Tortoise.init(db_url=settings.DATABASE_URL, modules=settings.TORTOISE_MODELS)
    await Tortoise.generate_schemas()

    # Parsing the json data
    with open(JSON_DATA_PATH, "r") as f:
        raw_json = f.read()
        data = json.loads(raw_json)

    # Creating the elements
    await create_users(data["users"])
    await create_tags(data["tags"])
    await create_apis(data["apis"])

    print("Success, the database was successfully populated!")


run_async(seed_db())
