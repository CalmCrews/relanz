from django.shortcuts import render
from user.models import User

# Create your views here.

def home(request):
    user=request.user
    if request.user.is_authenticated:
        return render(request, 'main/home.html', {'user':user})
    return render(request, 'main/home.html')