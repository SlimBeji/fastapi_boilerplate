from typing import Union

from fastapi import APIRouter

index_router = APIRouter(prefix="/api")


@index_router.get("/")
def read_root():
    return {"Hello": "World"}


@index_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
