from django.conf import settings
from django.db import models
import uuid

from django.db.models import constraints

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
        related_name='course_of_student',
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

class AssignmentModule(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'course'],
                name='unique name'
            )
        ]

class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments_of_course'
    )
    grouping = models.ForeignKey(
        AssignmentModule,
        on_delete=models.CASCADE,
        related_name='assignments_of_grouping',
        null=True
    )
    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    description = models.TextField(max_length=10000, blank=True)
    total_points = models.FloatField(null=True, blank=True)

class Grade(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grade_of_student"
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="grade_of_assignment"
    )
    earned_points = models.FloatField(null=True, blank=True)
    feedback = models.CharField(max_length=1000, null=True, blank=True)

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
    details = models.TextField(max_length=10000, blank=True)
    submit_datetime = models.DateTimeField(auto_now_add=True, blank=True)