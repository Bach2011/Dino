from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name='login'),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("play/<int:id>", views.play, name="play"),
    path("quiz/<int:id>/create", views.create_question, name="create_question"),
    path("quiz/create", views.create_quiz, name="create_quiz"),
    path("quiz/<int:id>", views.edit, name="edit_quiz"),
    path('quizzes', views.quizzes, name="quizzes"),

]
