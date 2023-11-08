from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from backend.dependencies import PaginationParams, apiitem_lookup, comma_joined_tags
from backend.models.api_item.model import ApiItem
from backend.models.api_item.schemas import (
    ApiItemGet,
    ApiItemInDB,
    ApiItemPost,
    ApiItemPut,
    ApiItemSearch,
)
from backend.models.tag.model import Tag
from backend.models.utils import filter_on_tags

api_item_router = APIRouter(prefix="/api/items", tags=["API items"])


@api_item_router.get("/", response_model=Page[ApiItemGet])
async def search_api_items(
    tags: str = Depends(comma_joined_tags),
    search: ApiItemSearch = Depends(),
    params: PaginationParams = Depends(),
):
    filters = search.model_dump(exclude_unset=True, exclude_none=True)
    result = await filter_on_tags(ApiItem, filters, tags, params)
    return result


@api_item_router.post("/", response_model=ApiItemGet)
async def post_api_item(api_item: ApiItemPost):
    data = api_item.model_dump(exclude_none=True, exclude_unset=True)
    tags = data.pop("tags", [])

    tag_records = []
    for tag in tags:
        tag_record, _ = await Tag.get_or_create(text=tag)
        tag_records.append(tag_record)

    item = await ApiItem.create(**data)
    await item.tags.add(*tag_records)

    return await ApiItemInDB.from_tortoise_orm(item)


@api_item_router.get("/{id}", response_model=ApiItemGet)
async def get_api_item(item: ApiItem = Depends(apiitem_lookup)):
    result = await ApiItemInDB.from_tortoise_orm(item)
    return result


@api_item_router.put("/{id}", response_model=ApiItemGet)
async def edit_api_item(
    data: ApiItemPut,
    item: ApiItem = Depends(apiitem_lookup),
):
    update_fields = data.model_dump(exclude_none=True, exclude_unset=True)
    tags = update_fields.pop("tags", [])

    tag_records = []
    for tag in tags:
        tag_record, _ = await Tag.get_or_create(text=tag)
        tag_records.append(tag_record)

    await item.tags.add(*tag_records)
    item = await item.update_from_dict(update_fields)
    await item.save()
    result = await ApiItemInDB.from_tortoise_orm(item)
    return result


@api_item_router.delete("/{id}")
async def delete_api_item(
    item: ApiItem = Depends(apiitem_lookup),
):
    await item.delete()
    return {"message": "success"}
