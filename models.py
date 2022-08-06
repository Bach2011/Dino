from django.db import models
from django.contrib.auth.models import AbstractUser
    # Create your models here.
class User(AbstractUser):
        pass
class Question(models.Model):
        quiz_id = models.IntegerField(default=1)
        title = models.CharField(max_length=100)
        point = models.IntegerField(default=1)
        def __str__ (self):
                return f"question: {self.title} id: {self.id}"
class Quiz(models.Model):
        name = models.CharField(max_length=1000, default="Quiz")
        question = models.ManyToManyField(Question,related_name="questions", blank=True, null=True)
        max_point = models.IntegerField(blank=True, null=True, default=0)
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
        def __str__ (self):
                return f"{self.id} Quiz: {self.name}"
class Answer(models.Model):
        choices_id = models.IntegerField()
        true = models.BooleanField(default=False)
        response_id = models.IntegerField(default=1)
        quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, name="quiz", blank=True, null=True)
        
class Response(models.Model):
        answer = models.ManyToManyField(Answer, blank=True, null=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        quiz_id = models.IntegerField(default=1)
        point = models.IntegerField(default=1)
        def __str__ (self):
                return f"Response from {self.user}"
class Choices(models.Model):
        choice = models.CharField(max_length=100)
        question_id = models.IntegerField(default=1)
        true = models.BooleanField(default=False)
