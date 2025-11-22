from django.urls import path

from . import views

app_name = "flood"

urlpatterns = [
    path("", views.flood_home, name="home"),
    path("plot/<str:handle>/", views.flood_plot, name="plot"),
    path("api/uplinks/", views.api_uplinks, name="api_uplinks"),
    path("api/history/", views.api_history, name="api_history"),
]


