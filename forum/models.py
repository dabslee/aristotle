from django.conf import settings
from django.db import models
import uuid

from django_quill.fields import QuillField

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
    coteachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='course_of_coteacher',
        blank=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return self.name

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
    
    def __str__(self):
        return self.name

class Assignment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments_of_course'
    )
    module = models.ForeignKey(
        AssignmentModule,
        on_delete=models.SET_NULL,
        related_name='assignments_of_module',
        null=True
    )
    title = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    description = QuillField()
    total_points = models.FloatField(null=True, blank=True)
    class Meta:
        ordering = ['end_datetime']
    
    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.assignment.title + " [grade]"

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
    details = QuillField()
    submit_datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.assignment.title + " [submission] id: " + str(self.id)