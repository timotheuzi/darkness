from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("command/", views.command_view, name="command"),
    path("poll/", views.poll_view, name="poll"),
    path("map/", views.map_api_view, name="map_api"),
    path("player/info/", views.player_info_view, name="player_info"),
    path("guide/", views.user_guide_view, name="user_guide"),
]
