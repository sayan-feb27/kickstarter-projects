import http
from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from ninja import Router

from schemas.project import ProjectSchemaIn, ProjectSchemaOut, ProjectUpdateSchema
from services.project import project_service

router = Router()


@router.post("/")
async def create_project(request: HttpRequest, payload: ProjectSchemaIn):
    await project_service.create(obj_in=payload)
    return HttpResponse(status=http.HTTPStatus.CREATED)


@router.patch("/{obj_id}")
async def update_project(request: HttpRequest, obj_id: Any, payload: ProjectUpdateSchema):
    count = await project_service.update(obj_id=obj_id, obj_in=payload)
    if not count:
        return HttpResponse(status=http.HTTPStatus.NOT_MODIFIED)
    return HttpResponse(status=http.HTTPStatus.NO_CONTENT)


@router.get("/", response=list[ProjectSchemaOut])
async def read_projects(request: HttpRequest, limit: int = 100, offset: int = 0):
    # todo: проверь сколько запросов уходит
    return await project_service.get_multi(limit=limit, offset=offset)


@router.get("/{obj_id}", response=ProjectSchemaOut)
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
