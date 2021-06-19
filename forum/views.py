from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

from .models import Assignment, Course, Submission, Grade
from . import forms

import datetime

def dateConvert(date_in):
    try:
        date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
        date_processing = [int(v) for v in date_processing]
        return datetime.datetime(*date_processing)
    except ValueError:
        return None
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
        if self.grade.count() == 0:
            self.grade = Grade.objects.create(assignment=assignment, student=student)
        else:
            self.grade = self.grade.first()
        if self.grade.earned_points:
            self.grade = self.grade.earned_points
            self.percentgrade = float(self.grade) * 100 / float(assignment.total_points)
        else:
            self.grade = "--"
            self.percentgrade = "--"
        self.link = reverse("forum:viewsubmission", kwargs={"assignment_id":assignment.id, "student_id":student.id})
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
        assignment.total_points = request.POST['points'] if request.POST['points']!="" else None
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
        context["grade"] = Grade.objects.filter(Q(assignment_id=assignment_id) & Q(student=request.user))
        if context["grade"].count() == 0:
            context["grade"] = Grade.objects.create(assignment=context["assignment"], student=request.user)
        else:
            context["grade"] = context["grade"].first()
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

def viewsubmission(request, assignment_id=None, student_id=None):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    context["assignment"] = Assignment.objects.filter(id=assignment_id).first()
    context["student"] = User.objects.filter(id=student_id).first()
    context["grade"] = Grade.objects.filter(Q(assignment_id=assignment_id) & Q(student_id=student_id))
    if context["grade"].count() == 0:
        context["grade"] = Grade.objects.create(assignment=context["assignment"], student=context["student"])
    else:
        context["grade"] = context["grade"].first()
    if request.method == "POST":
        context["grade"].earned_points = request.POST['grade']
        context["grade"].feedback = request.POST['feedback']
        context["grade"].save()
        context["savedmessage"] = "Feedback saved!"
    context["submissions"] = Submission.objects.filter(Q(assignment_id=assignment_id) & Q(student_id=student_id)).order_by('-submit_datetime')
    return render(request, "viewsubmission.html", context)

def newassignment(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    if (course.owner != request.user):
        return redirect('home')
    if request.method == "POST":
        form = forms.CreateAssignmentForm(request.POST)
        if form.is_valid():
            Assignment.objects.create(
                title=form.cleaned_data['title'],
                start_datetime=form.cleaned_data['start_datetime'],
                end_datetime=form.cleaned_data['end_datetime'],
                description=form.cleaned_data['description'],
                total_points=form.cleaned_data['total_points'],
                course=course
            )
            return HttpResponseRedirect(reverse("forum:assignments"))
    else:
        context["form"] = forms.CreateAssignmentForm()
        return render(request, "newassignment.html", context)