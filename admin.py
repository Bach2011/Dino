from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Quiz)
admin.site.register(models.Response)
admin.site.register(models.Answer)
admin.site.register(models.RightAnswer)
admin.site.register(models.Choices)
admin.site.register(models.Question)