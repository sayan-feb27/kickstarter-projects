import http
from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from ninja import Router

from schemas.project import ProjectSchema
from services.project import project_service

router = Router()


@router.get("/", response=list[ProjectSchema])
async def read_projects(request: HttpRequest, limit: int = 100, offset: int = 0):
    # todo: проверь сколько запросов уходит
    return await project_service.get_multi(limit=limit, offset=offset)


@router.get("/{obj_id}", response=ProjectSchema)
async def read_project(request: HttpRequest, obj_id: Any):
    obj = await project_service.get(obj_id=obj_id)
    if not obj:
        raise Http404("Project does not exist.")
    return obj


@router.delete("/{obj_id}")
async def delete_project(request: HttpRequest, obj_id: Any):
    obj = await project_service.delete(obj_id=obj_id)
    if obj is None:
        raise Http404("Project does not exist.")
    return HttpResponse(status=http.HTTPStatus.NO_CONTENT)
