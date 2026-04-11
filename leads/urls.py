from django.urls import path
from . import views

urlpatterns = [
    path("", views.lead_list, name="lead_list"),
    path("new/", views.lead_create, name="lead_create"),
    path("<int:pk>/", views.lead_detail, name="lead_detail"),
    path("<int:pk>/edit/", views.lead_edit, name="lead_edit"),
    path("<int:pk>/delete/", views.lead_delete, name="lead_delete"),
]