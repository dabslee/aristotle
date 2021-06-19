from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template import RequestContext

def home(request):
    if request.user.is_authenticated:
        return redirect('forum:index')
    else:
        return render(request, 'home.html', {})

def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name, {})
    response.status_code = 404
    return response