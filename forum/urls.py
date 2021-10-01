from forum.views_folder import views_assignments, views_courses, views_modules, views_students, views_submissions
from django.urls import path

from .views_folder import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('course_id=<course_id>/', views.index, name='index'),
    
    path('course_id=<course_id>/students/', views_students.students, name='students'),
    path('course_id=<course_id>/students/grades/student_id=<student_id>/', views_students.studentgrades, name='studentgrades'),

    path('course_id=<course_id>/courses/', views_courses.courses, name='courses'),
    path('courses/', views_courses.courses, name='courses'),
    path('course_id=<course_id>/setcourse/', views_courses.setcourse, name='setcourse'),
    path('course_id=<course_id>/removefrompinned/', views_courses.removefrompinned, name='removefrompinned'),
    path('createcourse/', views_courses.createcourse, name='createcourse'),

    path('course_id=<course_id>/assignments/', views_assignments.assignments, name='assignments'),
    path('course_id=<course_id>/assignments/newassignment/', views_assignments.newassignment, name='newassignment'),
    path('course_id=<course_id>/assignments/assignment_id=<assignment_id>/delete/', views_assignments.delete_assignment, name='delete_assignment'),
    path('course_id=<course_id>/assignments/assignment_id=<assignment_id>/', views_assignments.assignmentdetails, name='assignmentdetails'),
    
    path('course_id=<course_id>/assignments/assignment_id=<assignment_id>/submit/', views_submissions.newsubmission, name='newsubmission'),
    path('course_id=<course_id>/assignments/submissions/assignment_id=<assignment_id>/student_id=<student_id>/', views_submissions.viewsubmission, name='viewsubmission'),
    
    path('course_id=<course_id>/modules/', views_modules.modules, name='modules'),
    path('course_id=<course_id>/createmodule/', views_modules.createmodule, name='createmodule'),
    path('course_id=<course_id>/deletemodule/module_id=<module_id>', views_modules.deletemodule, name='deletemodule'),
]
