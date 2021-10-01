from django.shortcuts import render, redirect

from ..models import Assignment, AssignmentModule, Course
from .. import forms

from .utilities import alwaysContext

class ModuleWrapper():
    def __init__(self, name, id, assignments):
        self.name = name
        self.id = id
        self.assignments = assignments
def modules(request, course_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    if request.method == "POST":
        for assn in Assignment.objects.filter(course=context["selected_course"]):
            if request.POST.get(f"assignment-checkbox-{assn.id}") == "checked":
                moduleid = int(request.POST.get("moduleassign"))
                if moduleid == 0:
                    assn.module = None
                else:
                    assn.module = AssignmentModule.objects.get(id=moduleid)
                assn.save()
    context["modules"] = [ModuleWrapper("No module", 0, Assignment.objects.filter(course=context["selected_course"], module=None))]
    for module in AssignmentModule.objects.filter(course=context["selected_course"]).order_by("name"):
        context["modules"].append(ModuleWrapper(module.name, module.id, Assignment.objects.filter(course=context["selected_course"], module=module).order_by("end_datetime")))
    return render(request, "modules.html", context)

def createmodule(request, course_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    if request.user != context["selected_course"].owner:
        return redirect('forum:modules')
    if request.method == 'POST':
        form = forms.CreateModuleForm(request.POST)
        if form.is_valid():
            AssignmentModule.objects.create(
                name=form.cleaned_data['name'],
                course = context["selected_course"]
            )
            return redirect("forum:modules")
    else:
        context["form"] = forms.CreateModuleForm()
        return render(request, "createmodule.html", context)

def deletemodule(request, course_id, module_id):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    if request.user != context["selected_course"].owner:
        return redirect('forum:modules')
    AssignmentModule.objects.get(id=module_id).delete()
    return redirect("forum:modules")