# About this project

This is a FastAPI boilerplate meant for learning purposes.

## Stack
- [FastAPI](https://fastapi.tiangolo.com/) for building Apps and APIs
- [Tortoise-ORM](https://tortoise-orm.readthedocs.io/en/latest/) as DB ORM
- [Aerich](https://github.com/tortoise/aerich) as Tortoise-ORM migration tool
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation, serialization, etc ...
- [Docker-Compose](https://docs.docker.com/compose/) for using Postgres and Redis locally
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) for templating.

## How to run the app

1. Create a `.env` file in root directory as follows

```
PYTHONPATH=/app
DATABASE_URL=postgres://docker:docker@db:5432/docker
REDIS_URL=redis://redis:6379/
ENV=local
```

2. Run docker-compose

```docker-compose up```

## How to use Aerich to setup the Database

### Case 1: New project

When starting a new project, no migration scripts were previously generated and the /migrations is empty

- Step 1: Start the docker-compose network with `make run`
- Step 2: Create the db with `make create-db`

### Case 2: Using existing scripts

If you want to clean up the dev database and start afresh, then we should use the generated migrations scripts inside the /migrations folder

- Step 1: Stop docker-compose from running
- Step 2: Run `make dump-db`. This will delete the data store inside the mapped /db folder
- Step 3: Rerun the docker-compose network with `make run`
- Step 4: Recreate the db with `make recreate-db`
