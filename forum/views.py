from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Assignment, Course
from . import forms

def alwaysContext(request):
    return {
        "username": request.user.username,
        "selected_course": Course.objects.filter(id=request.session.get('selected_course_id')).first()
    }

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    return render(request, "index.html", context)

def courses(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    if request.method == 'POST':
        form = forms.JoinCourseForm(request.POST)
        if form.is_valid():
            uuid=form.cleaned_data['uuid']
            course = Course.objects.get(uuid=uuid)
            course.students.add(request.user)
            return redirect("forum:courses")
        else:
            context["error"] = "Course not found."
    context["courses"] = Course.objects.filter(Q(owner=request.user) | Q(students=request.user)).distinct()
    context["form"] = forms.JoinCourseForm()
    return render(request, "courses.html", context)

def setcourse(request, course_id):
    if not request.user.is_authenticated:
        return redirect('home')
    request.session['selected_course_id'] = course_id
    return redirect("forum:courses")

def students(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    context["students"] = User.objects.filter(course_of_student=course)
    return render(request, "students.html", context)

def createcourse(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.CreateCourseForm(request.POST)
        if form.is_valid():
            Course.objects.create(
                name=form.cleaned_data['name'],
                owner=request.user
            )
            return redirect("forum:courses")
    else:
        context = alwaysContext(request)
        context["form"] = forms.CreateCourseForm()
        return render(request, "createcourse.html", context)

def assignments(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    context["assignments"] = Assignment.objects.filter(course=course)
    if (course.owner == request.user):
        return render(request, "assignments_teacher.html", context)
    else:
        return render(request, "assignments_student.html", context)