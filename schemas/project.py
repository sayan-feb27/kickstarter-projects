from ninja import ModelSchema

from projects.models import Category, Country, Project


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = "__all__"


class CountrySchema(ModelSchema):
    class Config:
        model = Country
        model_fields = "__all__"


class ProjectSchema(ModelSchema):
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
