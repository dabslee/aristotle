from django.shortcuts import render, redirect

from ..models import Assignment, AssignmentModule, Course
from .. import forms

from .utilities import alwaysContext

class ModuleWrapper():
    def __init__(self, name, id, assignments):
        self.name = name
        self.id = id
        self.assignments = assignments
def modules(request):
    if not request.user.is_authenticated:
        return redirect('home')        
    context = alwaysContext(request)
    course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
    if request.method == "POST":
        for assn in Assignment.objects.filter(course=course):
            if request.POST.get(f"assignment-checkbox-{assn.id}") == "checked":
                assn.module = AssignmentModule.objects.get(id=int(request.POST.get("moduleassign")))
                assn.save()
    context["modules"] = [ModuleWrapper("No module", 0, Assignment.objects.filter(course=course, module=None))]
    for module in AssignmentModule.objects.filter(course=course):
        context["modules"].append(ModuleWrapper(module.name, module.id, Assignment.objects.filter(course=course, module=module).order_by("end_datetime")))
    return render(request, "modules.html", context)

def createmodule(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = forms.CreateModuleForm(request.POST)
        if form.is_valid():
            AssignmentModule.objects.create(
                name=form.cleaned_data['name'],
                course = Course.objects.filter(id=request.session.get('selected_course_id')).first()
            )
            return redirect("forum:modules")
    else:
        context = alwaysContext(request)
        context["form"] = forms.CreateModuleForm()
        return render(request, "createmodule.html", context)