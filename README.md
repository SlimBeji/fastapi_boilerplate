# About this project

This is a FastAPI boilerplate meant for learning purposes.

## Stack
- [FastAPI](https://fastapi.tiangolo.com/) for building Apps and APIs
- [Tortoise-ORM](https://tortoise-orm.readthedocs.io/en/latest/) as DB ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation, serialization, etc ...
- [Docker-Compose](https://docs.docker.com/compose/) for using Postgres and Redis locally
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) for templating.

## How to run the app

1. Create a `.env` file in root directory as follows

```
DATABASE_URL=postgres://docker:docker@db:5432/docker
REDIS_URL=redis://redis:6379/
```

2. Run docker-compose

```docker-compose up```

## Scripts

### seed_db

This script is for deleting/creating/poulating database with records.

To run, withing the project root directory:
```
docker exec -it fastapi_boilerplate_web_1 bash
python -m postman.scripts.seed_db
```