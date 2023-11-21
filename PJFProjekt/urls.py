from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("PhoneService/", include("PhoneService.urls")),
    path("admin/", admin.site.urls),
]

