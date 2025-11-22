from django.urls import path

from . import views

app_name = "fleet"

urlpatterns = [
    path("", views.vehicle_list, name="vehicle_list"),
    path("vehicles/new/", views.vehicle_create, name="vehicle_create"),
    path("vehicles/<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path(
        "vehicles/<int:vehicle_pk>/defects/new/",
        views.defect_create,
        name="defect_create_for_vehicle",
    ),
    path("defects/new/", views.defect_create, name="defect_create"),
    path(
        "vehicles/<int:vehicle_pk>/maintenance/new/",
        views.maintenance_create,
        name="maintenance_create_for_vehicle",
    ),
    path("maintenance/new/", views.maintenance_create, name="maintenance_create"),
]


