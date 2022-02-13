from fastapi import APIRouter
from starlette.requests import Request

from postman.config import templates

dashboard_router = APIRouter()


@dashboard_router.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})
