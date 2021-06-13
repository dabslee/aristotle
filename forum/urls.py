from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('setcourse/<course_id>', views.setcourse, name='setcourse'),
    path('students/', views.students, name='students'),
    path('createcourse/', views.createcourse, name='createcourse'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignments/<assignment_id>', views.assignmentdetails, name='assignmentdetails'),
    path('assignments/<assignment_id>/submit', views.newsubmission, name='newsubmission'),
]
