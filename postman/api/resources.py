from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_pagination import Page, Params, paginate

from postman.config import settings
from postman.models import ApiItem, Endpoint, QueryParam, Tag
from postman.schemas.models import (
    ApiItemPydanticGet,
    ApiItemPydanticPost,
    ApiItemPydanticPut,
    EndpointPydanticGet,
    EndpointPydanticPost,
    EndpointPydanticPut,
    QueryParamPydanticGet,
    QueryParamPydanticPost,
    QueryParamPydanticPut,
)

TAGS_REGEX = r"^\w*(,\w*)*$"

resources_router = APIRouter(prefix="/api/resources")


class MyParams(Params):
    size: int = Query(
        settings.MAX_ITEM_PER_RESPONSE, ge=1, le=100, description="Page size"
    )


def tags_param(tags: Optional[str] = Query(None, regex=TAGS_REGEX)):
    return tags


def tags_path_param(tags: str = Path(..., regex=TAGS_REGEX)):
    return tags


@resources_router.get(
    "/apis/", response_model=Page[ApiItemPydanticGet], tags=["api"]
)
async def get_all_api_items(
    params: MyParams = Depends(),
    tags: Optional[str] = Depends(tags_param),
):
    filters = {}
    if tags:
        splited_tags = [t.strip() for t in tags.split(",")]
        filters = {"tags__text__in": splited_tags}

    items = await ApiItemPydanticGet.from_queryset(
        ApiItem.filter(**filters).prefetch_related("tags")
    )

    return paginate(items, params)


@resources_router.post(
    "/apis/", response_model=ApiItemPydanticGet, tags=["api"]
)
async def post_api_item(
    api_item: ApiItemPydanticPost, tags: Optional[str] = Depends(tags_param)
):
    tag_records = []
    if tags:
        for tag in tags.split(","):
            tag = tag.strip()
            tag_record, _ = await Tag.get_or_create(text=tag)
            tag_records.append(tag_record)

    item = await ApiItem.create(**api_item.dict(exclude_unset=True))
    await item.tags.add(*tag_records)
    return await ApiItemPydanticGet.from_tortoise_orm(item)


async def apiitem_lookup(id):
    record = await ApiItem.filter(id=id).prefetch_related("tags").first()
    if record:
        return record
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )


@resources_router.get(
    "/apis/{id}", response_model=ApiItemPydanticGet, tags=["api"]
)
async def get_api_item(id: int):
    record = await apiitem_lookup(id)
    item = await ApiItemPydanticGet.from_tortoise_orm(record)
    return item


@resources_router.put(
    "/apis/{id}", response_model=ApiItemPydanticGet, tags=["api"]
)
async def edit_api_item(
    id: int,
    data: ApiItemPydanticPut,
    tags: Optional[str] = Depends(tags_param),
):
    record = await apiitem_lookup(id)

    tag_records = []
    if tags:
        for tag in tags.split(","):
            tag = tag.strip()
            tag_record, _ = await Tag.get_or_create(text=tag)
            tag_records.append(tag_record)

    await record.tags.add(*tag_records)
    record = record.update_from_dict(data.dict(exclude_unset=True))
    await record.save()
    item = await ApiItemPydanticGet.from_tortoise_orm(record)
    return item


@resources_router.delete("/apis/{id}", tags=["api"])
async def delete_api_item(id: int):
    record = await apiitem_lookup(id)
    await record.delete()
    return {"message": "success"}


@resources_router.delete("/apis/{id}/tags/{tags}", tags=["api"])
async def delete_api_item_tag(
    id: int,
    tags: str = Depends(tags_path_param),
):
    record = await apiitem_lookup(id)
    tags_requested_to_be_deleted = [t.strip() for t in tags.split(",")]

    tags_to_remove = []
    for tag in record.tags:
        if tag.text in tags_requested_to_be_deleted:
            tags_to_remove.append(tag)

    await record.tags.remove(*tags_to_remove)
    return {"message": "success"}


@resources_router.get(
    "/apis/{id}/endpoints",
    response_model=Page[EndpointPydanticGet],
    tags=["endpoints"],
)
async def get_api_endpoints(
    id: int,
    tags: Optional[str] = Depends(tags_param),
    params: MyParams = Depends(),
):
    filters = {"api_item_id": id}
    if tags:
        splited_tags = [t.strip() for t in tags.split(",")]
        filters["tags__text__in"] = splited_tags

    data = await EndpointPydanticGet.from_queryset(Endpoint.filter(**filters))
    return paginate(data, params)


@resources_router.post(
    "/apis/{id}/endpoints",
    response_model=EndpointPydanticGet,
    tags=["endpoints"],
)
async def create_new_endpoint(id: int, endpoint: EndpointPydanticPost):
    await apiitem_lookup(id)
    data = endpoint.dict(exclude_unset=True)

    tag_records = []
    tags = data.pop("tags")
    if tags:
        for tag in tags.split(","):
            tag = tag.strip()
            tag_record, _ = await Tag.get_or_create(text=tag)
            tag_records.append(tag_record)

    item = await Endpoint.create(**data, api_item_id=id)
    await item.tags.add(*tag_records)
    return await EndpointPydanticGet.from_tortoise_orm(item)


async def endpoint_lookup(apiitem_id, endpoint_id, prefitch=True):
    query = Endpoint.filter(id=endpoint_id, api_item_id=apiitem_id)
    if prefitch:
        query = query.prefetch_related("tags")

    record = await query.first()
    if record:
        return record
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )


@resources_router.get(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}",
    response_model=EndpointPydanticGet,
    tags=["endpoints"],
)
async def get_endpoint(apiitem_id: int, endpoint_id: int):
    endpoint = await endpoint_lookup(apiitem_id, endpoint_id)
    return EndpointPydanticGet.from_orm(endpoint)


@resources_router.put(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}",
    response_model=EndpointPydanticGet,
    tags=["endpoints"],
)
async def edit_endpoint_item(
    apiitem_id: int,
    endpoint_id: int,
    data: EndpointPydanticPut,
    tags: Optional[str] = Depends(tags_param),
):
    record = await endpoint_lookup(apiitem_id, endpoint_id)
    tag_records = []
    if tags:
        for tag in tags.split(","):
            tag = tag.strip()
            tag_record, _ = await Tag.get_or_create(text=tag)
            tag_records.append(tag_record)

    await record.tags.add(*tag_records)
    record = record.update_from_dict(data.dict(exclude_unset=True))
    await record.save()
    item = await EndpointPydanticGet.from_tortoise_orm(record)
    return item


@resources_router.delete(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}",
    tags=["endpoints"],
)
async def delete_endpoint_item(apiitem_id: int, endpoint_id: int):
    endpoint = await endpoint_lookup(apiitem_id, endpoint_id)
    await endpoint.delete()
    return {"message": "success"}


@resources_router.delete(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/tags/{tags}",
    tags=["endpoints"],
)
async def delete_endpoint_tags(
    apiitem_id: int,
    endpoint_id: int,
    tags: str = Depends(tags_path_param),
):
    record = await endpoint_lookup(apiitem_id, endpoint_id)
    tags_requested_to_be_deleted = [t.strip() for t in tags.split(",")]

    tags_to_remove = []
    for tag in record.tags:
        if tag.text in tags_requested_to_be_deleted:
            tags_to_remove.append(tag)

    await record.tags.remove(*tags_to_remove)
    return {"message": "success"}


@resources_router.get(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/query_params",
    response_model=Page[QueryParamPydanticGet],
    tags=["query_params"],
)
async def get_all_query_params(
    apiitem_id: int,
    endpoint_id: int,
    params: MyParams = Depends(),
):
    await endpoint_lookup(apiitem_id, endpoint_id, prefitch=False)
    data = await QueryParamPydanticGet.from_queryset(
        QueryParam.filter(endpoint_id=endpoint_id)
    )
    return paginate(data, params)


@resources_router.post(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/query_params",
    response_model=QueryParamPydanticGet,
    tags=["query_params"],
)
async def create_new_query_param(
    apiitem_id: int, endpoint_id: int, query_param: QueryParamPydanticPost
):
    await endpoint_lookup(apiitem_id, endpoint_id, prefitch=False)
    data = query_param.dict(exclude_unset=True)
    item = await QueryParam.create(**data, endpoint_id=endpoint_id)
    return await QueryParamPydanticGet.from_tortoise_orm(item)


async def query_param_lookup(
    apiitem_id, endpoint_id, query_param_id, prefitch=True
):
    query = QueryParam.filter(id=query_param_id, endpoint_id=endpoint_id)

    if prefitch:
        record = await query.prefetch_related("endpoint").first()
        if record and record.endpoint.api_item_id == apiitem_id:
            return record
    else:
        record = await query.first()
        if record:
            return record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    )


@resources_router.get(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/query_params/{id}",
    response_model=QueryParamPydanticGet,
    tags=["query_params"],
)
async def get_query_param(apiitem_id: int, endpoint_id: int, id: int):
    record = await query_param_lookup(apiitem_id, endpoint_id, id)
    return QueryParamPydanticGet.from_orm(record)


@resources_router.put(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/query_params/{id}",
    response_model=QueryParamPydanticGet,
    tags=["query_params"],
)
async def edit_query_param_item(
    apiitem_id: int,
    endpoint_id: int,
    id: int,
    data: QueryParamPydanticPut,
):
    record = await query_param_lookup(apiitem_id, endpoint_id, id)
    record = record.update_from_dict(data.dict(exclude_unset=True))
    await record.save()
    item = await QueryParamPydanticGet.from_tortoise_orm(record)
    return item


@resources_router.delete(
    "/apis/{apiitem_id}/endpoints/{endpoint_id}/query_params/{id}",
    tags=["query_params"],
)
async def delete_query_param_item(
    apiitem_id: int,
    endpoint_id: int,
    id: int,
):
    record = await query_param_lookup(apiitem_id, endpoint_id, id)
    await record.delete()
    return {"message": "success"}
