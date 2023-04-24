from projects.models import Project

from .base import Service


class ProjectService(Service):
    async def get_queryset(self):
        qs = await super().get_queryset()
        return qs.select_related("category", "sub_category", "country")


project_service = ProjectService(model=Project)
