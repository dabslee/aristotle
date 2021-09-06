from forum.views_folder.utilities import alwaysContext
from django.shortcuts import render, redirect
from ..models import Assignment
from django.db.models import Q
import datetime

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    context["assignments"] = Assignment.objects.filter(
        Q(course__owner=request.user)
        | Q(course__students=request.user)
        & Q(end_datetime__gte=str(datetime.datetime.now()))
        & Q(end_datetime__lte=str(datetime.datetime.now() + datetime.timedelta(days=7)))
    ).exclude(
        end_datetime__isnull=True
    )
    return render(request, "index.html", context)