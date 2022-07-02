from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name='login'),
    path("register", views.register, name="register"),
    path("play", views.play, name="play"),
    path("create", views.create, name="create")
]
