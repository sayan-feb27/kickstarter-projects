from django.db import models

from core.mixins import TimeStampedModel, UUIDMixin


class Category(models.Model):
    name = models.CharField(verbose_name="Category name", primary_key=True, max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(verbose_name="Country name", primary_key=True, max_length=100)
    code2 = models.CharField(verbose_name="Two letter code", blank=True, null=True, max_length=2)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Project(UUIDMixin, TimeStampedModel):
    class ProjectState(models.IntegerChoices):
        LIVE = 0, "Live"
        CANCELLED = 1, "Cancelled"
        SUSPENDED = 2, "Suspended"
        FAILED = 3, "Failed"
        SUCCESSFUL = 4, "Successful"

        __empty__ = "(Unknown)"

    external_id = models.BigIntegerField(verbose_name="External id", unique=True)
    name = models.CharField(verbose_name="Name", max_length=200)

    category = models.ForeignKey(verbose_name="Category", to="Category", on_delete=models.RESTRICT, related_name="+")
    sub_category = models.ForeignKey(
        verbose_name="Sub-category", to="Category", on_delete=models.RESTRICT, related_name="+"
    )
    country = models.ForeignKey(
        verbose_name="Country of product origin",
        to="Country",
        on_delete=models.RESTRICT,
        related_name="+",
    )

    launch_date = models.DateField(verbose_name="Date the project was launched")
    deadline_date = models.DateField(verbose_name="Deadline for crowdfunding")
    goal = models.DecimalField(
        verbose_name="Amount of money the creater needs to complete the project (USD)",
        max_digits=20,
        decimal_places=2,
        default=0,
    )
    pledged = models.DecimalField(
        verbose_name="Amount of money pledged to by the crowd (USD)", max_digits=20, decimal_places=2, default=0
    )
    backers = models.IntegerField(verbose_name="Number of backers", default=0)
    state = models.IntegerField(
        verbose_name="Current condition the project", choices=ProjectState.choices, blank=True, null=True
    )

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.name} ({self.external_id})"
