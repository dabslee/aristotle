from forum.views_folder import views_assignments, views_courses, views_modules, views_students, views_submissions
from django.urls import path

from .views_folder import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    
    path('students/', views_students.students, name='students'),
    path('students/grades/<student_id>', views_students.studentgrades, name='studentgrades'),

    path('courses/', views_courses.courses, name='courses'),
    path('setcourse/<course_id>', views_courses.setcourse, name='setcourse'),
    path('createcourse/', views_courses.createcourse, name='createcourse'),

    path('assignments/', views_assignments.assignments, name='assignments'),
    path('assignments/newassignment', views_assignments.newassignment, name='newassignment'),
    path('assignments/<assignment_id>/delete', views_assignments.delete_assignment, name='delete_assignment'),
    path('assignments/<assignment_id>', views_assignments.assignmentdetails, name='assignmentdetails'),
    
    path('assignments/<assignment_id>/submit', views_submissions.newsubmission, name='newsubmission'),
    path('assignments/submissions/assignment_id=<assignment_id>/student_id=<student_id>', views_submissions.viewsubmission, name='viewsubmission'),
    
    path('modules/', views_modules.modules, name='modules'),
    path('createmodule/', views_modules.createmodule, name='createmodule'),
]
