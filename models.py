from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
class Question(models.Model):
    title = models.TextField(max_length=100)
class Quiz(models.Model):
    questions = models.ForeignKey(Question, on_delete=CASCADE, related_name="questions")
class Answer(models.Model):
    correct_answer = models.TextField(max_length=100)
class Response(models.Model):
    answer = models.TextField(max_length=100)
class Choices(models.Model):
    choice1 = models.TextField(max_length=100)
    choice2 = models.TextField(max_length=100)
    choice3 = models.TextField(max_length=100, blank=True, null=True)
    choice4 = models.TextField(max_length=100, blank=True, null=True)