from django.conf import settings
from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_of_owner'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='course_of_student'
    )

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.CharField(max_length=10000)
    total_points = models.IntegerField(null=True, blank=True)

class Submission(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submission_of_student"
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submission_of_assignment"
    )
    earned_points = models.IntegerField(null=True, blank=True)