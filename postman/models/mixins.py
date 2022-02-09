import asyncpg
from tortoise import fields
from tortoise.models import Model

from postman.config import get_settings
from postman.utils.helpers import parse_db_url


async def destroy_db():
    """Destroying the database with brute force
    Used for seeding testing databases"""

    settings = get_settings()
    parsed_db_url = parse_db_url(settings.DATABASE_URL)
    user = parsed_db_url.get("user")
    password = parsed_db_url.get("password")
    host = parsed_db_url.get("host")
    port = parsed_db_url.get("port")
    db = parsed_db_url.get("db")

    conn = await asyncpg.connect(
        user=user,
        password=password,
        database="postgres",
        host=host,
        port=port,
    )

    create_script = f"""
    CREATE DATABASE {db} OWNER {user}
    """
    limit_connection_script = f"""
    ALTER DATABASE {db} CONNECTION LIMIT 0;
    """

    kill_connections_script = f"""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '{db}';
    """

    drop_database_script = f"""
    DROP DATABASE {db};
    """

    await conn.execute(limit_connection_script)
    await conn.execute(kill_connections_script)
    await conn.execute(drop_database_script)
    await conn.execute(create_script)
    await conn.close()


class TimeDataMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True)


class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    @classmethod
    async def get_by_id(cls, id):
        item = await cls.get(id=id)
        return item

    class Meta:
        abstract = True
