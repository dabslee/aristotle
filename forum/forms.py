from django import forms
from django.forms.widgets import Textarea
from .models import Course

class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=100)

class JoinCourseForm(forms.Form):
    uuid = forms.UUIDField()

class NewSubmission(forms.Form):
    details = forms.CharField(max_length=10000, widget=forms.Textarea)

class CreateAssignmentForm(forms.Form):
    title = forms.CharField(max_length=100)
    start_datetime = forms.DateTimeField(required=False)
    end_datetime = forms.DateTimeField(required=False)
    description = forms.CharField(max_length=10000, required=False, widget=Textarea)
    total_points = forms.FloatField(required=False)