from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "apiitem" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "label" VARCHAR(80) NOT NULL,
    "description" TEXT NOT NULL,
    "url" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "endpoint" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" TEXT NOT NULL,
    "label" VARCHAR(80) NOT NULL,
    "description" TEXT NOT NULL,
    "http_method" VARCHAR(5) NOT NULL  DEFAULT 'get',
    "api_item_id" INT NOT NULL REFERENCES "apiitem" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "endpoint"."http_method" IS 'GET: get\nPOST: post\npatch: patch\nput: push';
CREATE TABLE IF NOT EXISTS "queryparam" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "label" VARCHAR(80) NOT NULL,
    "type" VARCHAR(7) NOT NULL,
    "description" TEXT NOT NULL,
    "default" VARCHAR(200),
    "required" BOOL NOT NULL  DEFAULT False,
    "location" VARCHAR(6) NOT NULL,
    "endpoint_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "queryparam"."type" IS 'INTEGER: integer\nSTRING: string\nFLOAT: float';
COMMENT ON COLUMN "queryparam"."location" IS 'HEADER: header\nPATH: path\nQUERY: query\nBody: body';
CREATE TABLE IF NOT EXISTS "role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "level" INT NOT NULL,
    "description" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "tag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "password" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "active" BOOL NOT NULL  DEFAULT False,
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "tag_apiitem" (
    "apiitem_id" INT NOT NULL REFERENCES "apiitem" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tag_endpoint" (
    "endpoint_id" INT NOT NULL REFERENCES "endpoint" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
