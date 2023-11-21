from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Rejestracja/", views.create, name="Rejestracja"),
    path("Wyszukiwanie/", views.read, name="Wyszukiwanie"),
    path("Wyszukiwanie/<int:IMEI>", views.result_view_by_IMEI, name="results"),
    path("Wyszukiwanie/<str:nr_case>", views.result_view_by_case, name="results"),
    path("Edycja/", views.edit, name="Edycja"),
    path("Usuwanie/", views.delete, name="Usuwanie"),
]
