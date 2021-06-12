from django.conf import settings
from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student'
    )