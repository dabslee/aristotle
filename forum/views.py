from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from .models import Assignment, Course, Submission, Grade
from . import forms

import datetime

def dateConvert(date_in):
    date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    return datetime.datetime(*date_processing)
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
            if (course.owner == request.user):
                context["error"] = "You are the owner of this course!"
            else:
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

class SubmissionRow():
    def __init__(self, student, assignment):
        self.username = student.username
        self.nosubmissions = Submission.objects.filter(Q(assignment=assignment) & Q(student=student)).count()
        self.grade = Grade.objects.filter(Q(assignment=assignment) & Q(student=student))
        if self.grade.count() > 0:
            self.grade = self.grade.first()
            self.percentgrade = self.grade * 100 / assignment.total_points
        else:
            self.grade = "--"
            self.percentgrade = "--"
def assignmentdetails(request, assignment_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    assignment = Assignment.objects.get(id=assignment_id)
    if Course.objects.filter(id=request.session.get('selected_course_id')).first() != assignment.course:
        return redirect('home')
    
    if request.method == "POST":
        assignment.title = request.POST['title']
        assignment.start_datetime = dateConvert(request.POST['start'])
        assignment.end_datetime = dateConvert(request.POST['end'])
        assignment.description = request.POST['description']
        assignment.save()
        context["savedmessage"] = "Changes saved."
    
    context["assignment"] = assignment
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    if (course.owner == request.user):
        context["students"] = []
        for student in User.objects.filter(course_of_student=course):
            context["students"].append(SubmissionRow(student, assignment))
        return render(request, "assignmentdetails_teacher.html", context)
    else:
        context["submissions"] = Submission.objects.filter(Q(assignment=assignment) & Q(student=request.user)).order_by('-submit_datetime')
        return render(request, "assignmentdetails_student.html", context)

def newsubmission(request, assignment_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    assignment = Assignment.objects.get(id=assignment_id)
    if Course.objects.filter(id=request.session.get('selected_course_id')).first() != assignment.course:
        return redirect('home')
    if request.method == "POST":
        form = forms.NewSubmission(request.POST)
        if form.is_valid():
            Submission.objects.create(
                student = request.user,
                assignment = assignment,
                details = form.cleaned_data['details']
            )
            return HttpResponseRedirect(reverse("forum:assignmentdetails", args=(assignment_id,)))
    else:
        context["assignment"] = assignment
        context["form"] = forms.NewSubmission()
        return render(request, "newsubmission.html", context)
