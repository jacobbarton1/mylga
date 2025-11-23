from django.urls import path

from . import views

app_name = "fleet"

urlpatterns = [
    path("", views.vehicle_list, name="vehicle_list"),
    path("vehicles/new/", views.vehicle_create, name="vehicle_create"),
    path("vehicles/<int:pk>/", views.vehicle_detail, name="vehicle_detail"),
    path("vehicles/<int:pk>/edit/", views.vehicle_update, name="vehicle_update"),
    path("vehicles/<int:pk>/delete/", views.vehicle_delete, name="vehicle_delete"),
    path(
        "vehicles/<int:vehicle_pk>/defects/new/",
        views.defect_create,
        name="defect_create_for_vehicle",
    ),
    path("defects/new/", views.defect_create, name="defect_create"),
    path("defects/<int:pk>/", views.defect_detail, name="defect_detail"),
    path("defects/<int:pk>/edit/", views.defect_update, name="defect_update"),
    path(
        "vehicles/<int:vehicle_pk>/maintenance/new/",
        views.maintenance_create,
        name="maintenance_create_for_vehicle",
    ),
    path("maintenance/new/", views.maintenance_create, name="maintenance_create"),
    path("maintenance/<int:pk>/", views.maintenance_detail, name="maintenance_detail"),
    path(
        "maintenance/<int:pk>/edit/",
        views.maintenance_update,
        name="maintenance_update",
    ),
]
