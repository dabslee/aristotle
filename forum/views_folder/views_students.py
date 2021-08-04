from forum.views_folder.views_assignments import gradeRender
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from ..models import Assignment, Course

from .utilities import alwaysContext

def students(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    context["students"] = User.objects.filter(course_of_student=course)
    return render(request, "students.html", context)

def studentgrades(request, student_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    student = User.objects.get(id=student_id)
    if (course.owner == request.user):
        selected_assignments = Assignment.objects.filter(course=course).order_by("end_datetime")
        if request.method == "POST":
            selected_assignments = Assignment.objects.filter(course=course, module_id=request.POST["modulefilter"])
        context["student"] = student
        context["page_title"] = "Grades for " + student.username
        return gradeRender(student, request, context, course, selected_assignments)
    else:
        return redirect('home')