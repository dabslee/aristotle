from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('setcourse/<course_id>', views.setcourse, name='setcourse'),
    path('students/', views.students, name='students'),
    path('students/grades/<student_id>', views.studentgrades, name='studentgrades'),
    path('createcourse/', views.createcourse, name='createcourse'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignments/newassignment', views.newassignment, name='newassignment'),
    path('assignments/<assignment_id>', views.assignmentdetails, name='assignmentdetails'),
    path('assignments/<assignment_id>/submit', views.newsubmission, name='newsubmission'),
    path('assignments/<assignment_id>/delete', views.delete_assignment, name='delete_assignment'),
    path('assignments/submissions/assignment_id=<assignment_id>/student_id=<student_id>', views.viewsubmission, name='viewsubmission'),
    path('modules/', views.modules, name='modules'),
    path('createmodule/', views.createmodule, name='createmodule'),
]
