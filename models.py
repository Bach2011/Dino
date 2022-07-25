from django.db import models
from django.contrib.auth.models import AbstractUser
    # Create your models here.
class User(AbstractUser):
        pass
class Question(models.Model):
        quiz_id = models.IntegerField(default=1)
        title = models.CharField(max_length=100)
        right_answer_id = models.IntegerField(default=1)
        type = models.CharField(max_length=100)
        def __str__ (self):
                return f"question: {self.title}"
class Quiz(models.Model):
        name = models.CharField(max_length=1000, default="Quiz")
        question = models.ManyToManyField(Question,related_name="questions", blank=True, null=True)
        owner = models.ForeignKey(User, on_delete=models.CASCADE)
        def __str__ (self):
                return f"Quiz: {self.name}"
class Answer(models.Model):
        answer = models.CharField(max_length=1000, blank=True, null=True)
        choices_id = models.IntegerField()
        quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, name="quiz", blank=True, null=True)
class Response(models.Model):
        answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        quiz_id = models.IntegerField(default=1)
        def __str__ (self):
                return f"Response from {self.user}"
class Choices(models.Model):
        choice = models.CharField(max_length=100)
        question_id = models.IntegerField(default=1)
class TextAnswer(models.Model):
        answer = models.CharField(max_length=1000)
        question_id = models.IntegerField()
class RightAnswer(models.Model):
        answer = models.ForeignKey(TextAnswer, on_delete=models.CASCADE, blank=True, null=True)
        choice = models.ForeignKey(Choices, on_delete=models.CASCADE, blank=True, null=True)
        quiz_id = models.IntegerField(default=1)
        question_id = models.IntegerField(default=1)
