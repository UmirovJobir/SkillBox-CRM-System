from django.urls import path
from . import views

urlpatterns = [
    path("", views.advertisement_list, name="advertisement_list"),
    path("new/", views.advertisement_create, name="advertisement_create"),
    path("statistic/", views.advertisement_statistic, name="advertisement_statistic"),
    path("<int:pk>/", views.advertisement_detail, name="advertisement_detail"),
    path("<int:pk>/edit/", views.advertisement_edit, name="advertisement_edit"),
    path("<int:pk>/delete/", views.advertisement_delete, name="advertisement_delete"),
]