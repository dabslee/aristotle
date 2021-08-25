from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

from datetime import datetime

from ..models import Assignment, AssignmentModule, Course, Submission, Grade
from .. import forms

from .utilities import alwaysContext, dateConvert

class StudentAssignmentRow():
    def __init__(self, student, assignment):
        self.id=assignment.id
        self.title=assignment.title
        self.start_datetime=assignment.start_datetime
        self.end_datetime=assignment.end_datetime
        grade = Grade.objects.filter(Q(assignment=assignment) & Q(student=student)).first()
        if grade:
            self.earned_points=grade.earned_points
            self.cum_num=grade.earned_points if grade.earned_points else 0
            self.cum_den=assignment.total_points if (assignment.total_points and grade.earned_points) else 0
        else:
            self.earned_points=None
            self.cum_num=0
            self.cum_den=0
        self.total_points=assignment.total_points
        submissions = Submission.objects.filter(Q(assignment=assignment) & Q(student=student))
        self.submitted= submissions.count() > 0 or self.earned_points != None
class TeacherAssignmentRow():
    def __init__(self, assignment, request):
        self.id = assignment.id
        self.title = assignment.title
        self.start_datetime = assignment.start_datetime
        self.end_datetime = assignment.end_datetime
        self.submitted = 0
        course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
        for student in User.objects.filter(course_of_student=course):
            if Grade.objects.filter(student=student, assignment=assignment).exclude(earned_points=None, feedback=None).count() > 0 or Submission.objects.filter(student=student, assignment=assignment).count() > 0:
                self.submitted += 1
        self.nostudents = User.objects.filter(course_of_student=course).count()
        self.graded = Grade.objects.filter(Q(assignment=assignment) & ~Q(earned_points=None)).count()
def gradeRender(student, request, context, course, selected_assignments):
    context["modules"] = AssignmentModule.objects.filter(course=course)
    assignments = []
    cum_num = 0
    cum_den = 0
    for assignment in selected_assignments:
        row = StudentAssignmentRow(student, assignment)
        assignments.append(row)
        cum_num += row.cum_num
        cum_den += row.cum_den
    context["cum_num"] = cum_num
    context["cum_den"] = cum_den
    context["assignments"] = assignments
    return render(request, "assignments_student.html", context)
def assignments(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    selected_assignments = Assignment.objects.filter(course=course).order_by("end_datetime")
    if request.method == "POST":
        selected_assignments = Assignment.objects.filter(course=course, module_id=request.POST["modulefilter"]).order_by("end_datetime")
    if (course.owner == request.user):
        context["modules"] = AssignmentModule.objects.filter(course=course)
        context["assignments"] = []
        for assignment in selected_assignments:
            context["assignments"].append(TeacherAssignmentRow(assignment, request))
        return render(request, "assignments_teacher.html", context)
    else:
        context["page_title"] = "Assignments"
        return gradeRender(request.user, request, context, course, selected_assignments)

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
                course=course,
                module=AssignmentModule.objects.filter(name=form.cleaned_data['module'], course=course).first(),
            )
            return HttpResponseRedirect(reverse("forum:assignments"))
    else:
        context["modules"] = [module.name for module in AssignmentModule.objects.filter(course=course)]
        context["form"] = forms.CreateAssignmentForm()
        return render(request, "newassignment.html", context)

def delete_assignment(request, assignment_id):
    if not request.user.is_authenticated:
        return redirect('home')
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    if (course.owner != request.user):
        return redirect('home')
    Assignment.objects.filter(id=assignment_id).delete()
    return redirect('forum:assignments')

class SubmissionRow():
    def __init__(self, student, assignment):
        self.username = student.username
        self.nosubmissions = Submission.objects.filter(Q(assignment=assignment) & Q(student=student)).count()
        self.grade = Grade.objects.filter(Q(assignment=assignment) & Q(student=student))
        if self.grade.count() == 0:
            self.grade = Grade.objects.create(assignment=assignment, student=student)
        else:
            self.grade = self.grade.first()
        if self.grade.earned_points != None:
            self.grade = self.grade.earned_points
            if self.grade != None and assignment.total_points != None and assignment.total_points != 0:
                self.percentgrade = float(self.grade) * 100 / float(assignment.total_points)
            else:
                self.percentgrade = "--"
        else:
            self.grade = "--"
            self.percentgrade = "--"
        self.link = reverse("forum:viewsubmission", kwargs={"assignment_id":assignment.id, "student_id":student.id})
def assignmentdetails(request, assignment_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    assignment = Assignment.objects.get(id=assignment_id)
    course = Course.objects.get(id=request.session.get('selected_course_id'))
    if course != assignment.course:
        return redirect('home')

    if request.method == "POST":
        form = forms.CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment.title=form.cleaned_data['title']
            print(f"start_datetime: {form.cleaned_data['start_datetime']}")
            assignment.start_datetime=form.cleaned_data['start_datetime']
            print(f"assn start_datetime: {assignment.start_datetime}")

            assignment.end_datetime=form.cleaned_data['end_datetime']
            assignment.description=form.cleaned_data['description']
            assignment.total_points=form.cleaned_data['total_points']
            assignment.course=course
            assignment.module=AssignmentModule.objects.filter(name=form.cleaned_data['module'], course=course).first()
            assignment.save()
            context["savedmessage"] = "Changes saved."
    
    context["assignment"] = assignment
    context["modulename"] = assignment.module.name if assignment.module else "No module"
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    if (course.owner == request.user):
        context["students"] = []
        for student in User.objects.filter(course_of_student=course):
            context["students"].append(SubmissionRow(student, assignment))
        context["modules"] = [module.name for module in AssignmentModule.objects.filter(course=course)]
        context["form"] = forms.CreateAssignmentForm(initial={
            "title" : assignment.title,
            "start_datetime" : assignment.start_datetime,
            "end_datetime" : assignment.end_datetime,
            "description" : assignment.description,
            "total_points" : assignment.total_points,
            "module" : assignment.module
        })
        return render(request, "assignmentdetails_teacher.html", context)
    else:
        context["grade"] = Grade.objects.filter(Q(assignment_id=assignment_id) & Q(student=request.user))
        if context["grade"].count() == 0:
            context["grade"] = Grade.objects.create(assignment=context["assignment"], student=request.user)
        else:
            context["grade"] = context["grade"].first()
        context["submissions"] = Submission.objects.filter(Q(assignment=assignment) & Q(student=request.user)).order_by('-submit_datetime')
        return render(request, "assignmentdetails_student.html", context)