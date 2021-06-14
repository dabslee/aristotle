from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.Course)
admin.site.register(models.Assignment)
admin.site.register(models.Submission)
admin.site.register(models.Grade)