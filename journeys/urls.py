from django.urls import path

from . import views

app_name = "journeys"

urlpatterns = [
    path("", views.journey_list, name="journey_list"),
    path("new/", views.journey_create, name="journey_create"),
    path("<int:pk>/", views.journey_detail, name="journey_detail"),
    path(
        "<int:journey_pk>/checkpoints/new/",
        views.checkpoint_create,
        name="checkpoint_create",
    ),
    path(
        "checkpoints/<uuid:checkpoint_uuid>/checkin/",
        views.checkpoint_checkin,
        name="checkpoint_checkin",
    ),
]


