from django import forms
from .models import Course

class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=100)

class JoinCourseForm(forms.Form):
    uuid = forms.UUIDField()

class NewSubmission(forms.Form):
    details = forms.CharField(max_length=10000, widget=forms.Textarea)