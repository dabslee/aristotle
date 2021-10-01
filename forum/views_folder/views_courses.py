from django.shortcuts import render, redirect, reverse
from django.urls import reverse
from django.db.models import Q

from ..models import Course, UserData
from .. import forms

from .utilities import alwaysContext

def courses(request, course_id=None):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    if request.method == 'POST':
        form = forms.JoinCourseForm(request.POST)
        if form.is_valid():
            uuid=form.cleaned_data['uuid']
            course = Course.objects.get(uuid=uuid)
            if (course.owner == request.user):
                context["error"] = "You are the owner of this course!"
            else:
                course.students.add(request.user)
                return redirect("forum:courses")
        else:
            context["error"] = "Course not found."
    context["courses"] = Course.objects.filter(Q(owner=request.user) | Q(students=request.user)).distinct().order_by("name")
    context["form"] = forms.JoinCourseForm()
    return render(request, "courses.html", context)

def setcourse(request, course_id):
    if not request.user.is_authenticated:
        return redirect('home')
    return redirect(reverse("forum:courses", kwargs={'course_id' : course_id}))

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
        context = alwaysContext(request, course_id=None)
        context["form"] = forms.CreateCourseForm()
        return render(request, "createcourse.html", context)

def removefrompinned(request, course_id):
    if not request.user.is_authenticated:
        return redirect('home')
    userdata = UserData.objects.get(user=request.user)
    userdata.pinnedcourses.remove(Course.objects.get(uuid=course_id))
    return redirect("forum:index")