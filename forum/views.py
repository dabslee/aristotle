from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user.is_authenticated:
        return render(request, "index.html", {})
    else:
        return redirect('home')

def courses(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return redirect('home')