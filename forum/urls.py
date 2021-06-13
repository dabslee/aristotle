from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('setcourse/<course_id>', views.setcourse, name='setcourse'),
    path('students/', views.students, name='students')
]
