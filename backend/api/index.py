from fastapi import APIRouter

index_router = APIRouter(prefix="/api", tags=["Hello World"])


@index_router.get("/")
def hello_world():
    return {"Hello": "World"}
