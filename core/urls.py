from django.contrib import admin
from django.urls import path

from api.v1.base import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
]
