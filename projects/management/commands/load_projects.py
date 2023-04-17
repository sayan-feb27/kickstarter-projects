import asyncio
import datetime as dt
from decimal import Decimal
from typing import Any

import aiocsv
import aiofiles
from django.core.management.base import BaseCommand
from pydantic import BaseModel, Field, validator  # pylint: disable=no-name-in-module

from projects.models import Category, Country, Project


class RawProject(BaseModel):
    external_id: int = Field(alias="id")
    name: str
    category: str
    sub_category: str = Field(alias="subcategory")
    country: str
    launch_date: str | dt.datetime = Field(alias="launched")
    deadline_date: str | dt.datetime = Field(alias="deadline")
    goal: Decimal
    pledged: Decimal
    backers: int
    state: str | Project.ProjectState

    @validator("state")
    def state_must_be_enum(cls, v):  # pylint: disable=invalid-name,no-self-argument
        v = v.upper()
        v = v if v != "CANCELED" else "CANCELLED"
        return Project.ProjectState[v]

    @validator("launch_date", "deadline_date")
    def check_dates(cls, v: str):  # pylint: disable=invalid-name,no-self-argument
        return dt.datetime.fromisoformat(v)


class Command(BaseCommand):
    help = "Load projects data from a file"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="data file path", required=True)

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(file_path=options.get("file")))

    async def run(self, file_path: str):
        async for line in self.extract(file_path=file_path):
            raw_project = await self.transform(line)
            await self.load(raw_project)

    @staticmethod
    async def extract(file_path: str):
        async with aiofiles.open(file_path) as file:
            async for line in aiocsv.AsyncDictReader(file):
                yield line

    @staticmethod
    async def transform(raw_data: dict[str, Any]) -> RawProject:
        project = RawProject.parse_obj({k.lower(): v for k, v in raw_data.items()})
        return project

    @staticmethod
    async def load(raw_project: RawProject):
        payload = raw_project.dict()

        external_id = payload.pop("external_id")
        payload["country"], _ = await Country.objects.aget_or_create(name=payload.pop("country"))
        payload["category"], _ = await Category.objects.aget_or_create(name=payload.pop("category"))
        payload["sub_category"], _ = await Category.objects.aget_or_create(name=payload.pop("sub_category"))

        await Project.objects.aupdate_or_create(external_id=external_id, defaults=payload)
