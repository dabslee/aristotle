from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('forum:index')
    else:
        return render(request, 'home.html', {})