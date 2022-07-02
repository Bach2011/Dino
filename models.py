from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
class Question(models.Model):
    title = models.TextField(max_length=100)
class Quiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questions")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
class Answer(models.Model):
    correct_answer = models.TextField(max_length=100)
class Response(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Choices(models.Model):
    choice1 = models.TextField(max_length=100)
    choice2 = models.TextField(max_length=100)
    choice3 = models.TextField(max_length=100, blank=True, null=True)
    choice4 = models.TextField(max_length=100, blank=True, null=True)
class RightAnswer(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE, blank=True, null=True)