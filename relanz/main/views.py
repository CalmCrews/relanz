from django.shortcuts import render, redirect
from user.models import User

# Create your views here.

def welcome(request):
    if request.user.is_anonymous:
        return render(request, 'main/splashscreen.html')
    else:
        return redirect('main:home')



def home(request):
    user=request.user
    if request.user.is_authenticated:
        return render(request, 'main/home.html', {'user':user})
    return render(request, 'main/home.html')
