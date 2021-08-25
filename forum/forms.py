from django import forms
from django_quill.fields import QuillFormField

class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=100)

class CreateModuleForm(forms.Form):
    name = forms.CharField(max_length=100)

class JoinCourseForm(forms.Form):
    uuid = forms.UUIDField()

class NewSubmission(forms.Form):
    details = QuillFormField()

class CreateAssignmentForm(forms.Form):
    title = forms.CharField(max_length=100)
    start_datetime = forms.DateTimeField(required=False)
    end_datetime = forms.DateTimeField(required=False)
    description = QuillFormField()
    total_points = forms.FloatField(required=False)
    module = forms.CharField(required=False, widget=forms.Select)