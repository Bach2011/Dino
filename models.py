from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
class Question(models.Model):
    pass
class Quiz(models.Model):
    pass
class Answer(models.Model):
    pass
class Response(models.Model):
    pass