from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name='login'),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("play/<int:id>", views.play, name="play"),
    path("quiz/<int:id>/create", views.create_question, name="create_question"),
    path("quiz/create", views.create_quiz, name="create_quiz"),
    path("quiz/<int:id>", views.edit_quiz, name="edit_quiz"),
    path('quizzes', views.my_quizzes, name="my_quizzes"),
    path("quiz/<int:quiz_id>/question/<int:id>", views.edit_question, name="edit_question"),
    path("quizzes/play", views.quizzes, name="quizzes")

]
