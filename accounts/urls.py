from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.request_link, name="request_link"),
    path("login/sent/", views.link_sent, name="link_sent"),
    path("magic/<str:token>/", views.magic_login, name="magic_login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]


