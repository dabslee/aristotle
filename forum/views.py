from forum.views_folder.utilities import alwaysContext
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = alwaysContext(request)
    return render(request, "index.html", context)