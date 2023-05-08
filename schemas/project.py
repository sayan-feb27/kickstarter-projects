import datetime

from ninja import Field, ModelSchema, Schema

from projects.models import Category, Country, Project


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = "__all__"


class CountrySchema(ModelSchema):
    class Config:
        model = Country
        model_fields = "__all__"


class ProjectSchemaOut(ModelSchema):
    category: CategorySchema
    sub_category: CategorySchema
    country: CountrySchema
    state: str

    class Config:
        model = Project
        model_exclude = ["created", "modified", "state"]

    @staticmethod
    def resolve_state(obj: Project) -> str:
        return obj.get_state_display()


class ProjectSchemaIn(ModelSchema):
    category: str = Field(alias="category_id")
    sub_category: str = Field(alias="sub_category_id")
    country: str = Field(alias="country_id")

    class Config:
        model = Project
        model_exclude = ["uuid", "created", "modified"]


class ProjectUpdateSchema(Schema):
    category: str | None = Field(alias="category_id", default=None)
    sub_category: str | None = Field(alias="sub_category_id", default=None)
    country: str | None = Field(alias="country_id", default=None)
    external_id: int | None
    name: str | None
    launch_date: datetime.date | None
    deadline_date: datetime.date | None
    goal: int | None
    pledged: int | None
    backers: str | None
    state: str | None
