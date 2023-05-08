from typing import Any, Type, TypeVar

from asgiref.sync import sync_to_async
from django.db.models import Model as DjangoModel, QuerySet
from ninja import ModelSchema

DBModelType = TypeVar("DBModelType", bound=DjangoModel)  # pylint: disable=invalid-name


class BaseService:
    async def get(self, obj_id: Any):
        raise NotImplementedError

    async def get_multi(self, limit: int = 100, offset: int = 0):
        raise NotImplementedError

    async def create(self, obj_in: Any):
        raise NotImplementedError

    async def update(self, obj_id: Any, obj_in: Any):
        raise NotImplementedError

    async def delete(self, obj_id: Any):
        raise NotImplementedError

    async def get_queryset(self):
        raise NotImplementedError


class Service(BaseService):
    def __init__(self, model: Type[DBModelType]):
        self._model = model

    async def get_queryset(self) -> QuerySet:
        return await sync_to_async(self._model.objects.all)()

    async def get(self, obj_id: Any) -> DBModelType:
        base_qs = await self.get_queryset()
        return await base_qs.filter(pk=obj_id).afirst()

    async def get_multi(self, limit: int = 100, offset: int = 0) -> list[DBModelType]:
        qs = await self.get_queryset()
        qs = await sync_to_async(list)(qs[offset : offset + limit])
        return qs

    async def create(self, obj_in: ModelSchema):
        obj = await self._model.objects.acreate(**obj_in.dict(by_alias=True))
        return obj

    async def update(self, obj_id: Any, obj_in: ModelSchema) -> int:
        count = await self._model.objects.filter(pk=obj_id).aupdate(**obj_in.dict(by_alias=True, exclude_unset=True))
        return count

    async def delete(self, obj_id: Any) -> int | None:
        obj = await self._model.objects.filter(pk=obj_id).afirst()
        if not obj:
            return None
        count, _ = await obj.adelete()
        return count
