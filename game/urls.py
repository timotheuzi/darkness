from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('command/', views.command_view, name='command'),
]
