from ninja import NinjaAPI

from .projects import router as projects_router

api = NinjaAPI(version="1.0.0")

api.add_router(router=projects_router, prefix="projects", tags=["projects"])
