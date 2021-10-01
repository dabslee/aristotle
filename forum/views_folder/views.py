from forum.views_folder.utilities import alwaysContext
from django.shortcuts import render, redirect
from ..models import Assignment, Course, UserData
from django.db.models import Q
import datetime

# Create your views here.
def index(request, course_id=None):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request, course_id)
    context["assignments"] = Assignment.objects.filter(
        Q(course__owner=request.user)
        | Q(course__students=request.user)
    ).filter(
        end_datetime__range=[str(datetime.datetime.now()), str(datetime.datetime.now() + datetime.timedelta(days=7))]
    ).exclude(
        end_datetime__isnull=True
    )
    context["courses"] = Course.objects.filter(
        Q(owner=request.user)
        | Q(students=request.user)
    )
    if request.method == "POST" and "pinselect" in request.POST:
        pincourseid = int(request.POST["pinselect"])
        print(request.user.id)
        userdata = UserData.objects.get(user=request.user)
        userdata.pinnedcourses.add(Course.objects.get(id=pincourseid))
    context["pinnedcourses"] = Course.objects.filter(
        Q(userdata_of_pinnedcourse__user = request.user)
    )
    return render(request, "index.html", context)