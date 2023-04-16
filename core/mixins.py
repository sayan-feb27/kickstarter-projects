from django.db import models


class UUIDMixin(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", primary_key=True)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
