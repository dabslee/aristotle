from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

from ..models import Assignment, Course, Submission, Grade
from .. import forms

from .utilities import alwaysContext

def newsubmission(request, course_id, assignment_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    if context["selected_course"] != assignment.course:
        return redirect('home')
    if request.method == "POST":
        form = forms.NewSubmission(request.POST)
        if form.is_valid():
            Submission.objects.create(
                student = request.user,
                assignment = assignment,
                details = form.cleaned_data['details']
            )
            return HttpResponseRedirect(reverse("forum:assignmentdetails", kwargs={"assignment_id" : assignment_id, "course_id" : course_id}))
    else:
        context["assignment"] = assignment
        context["form"] = forms.NewSubmission()
        return render(request, "newsubmission.html", context)

def viewsubmission(request, course_id, assignment_id, student_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    context["assignment"] = Assignment.objects.filter(id=assignment_id).first()
    context["student"] = User.objects.filter(id=student_id).first()
    context["grade"] = Grade.objects.filter(Q(assignment_id=assignment_id) & Q(student_id=student_id))
    if context["grade"].count() == 0:
        context["grade"] = Grade.objects.create(assignment=context["assignment"], student=context["student"])
    else:
        context["grade"] = context["grade"].first()
    if request.method == "POST":
        context["grade"].earned_points = request.POST['grade'] if request.POST['grade'] else None
        context["grade"].feedback = request.POST['feedback'] if request.POST['feedback'] else None
        context["grade"].save()
        context["savedmessage"] = "Feedback saved!"
    context["submissions"] = Submission.objects.filter(Q(assignment_id=assignment_id) & Q(student_id=student_id)).order_by('-submit_datetime')
    return render(request, "viewsubmission.html", context)