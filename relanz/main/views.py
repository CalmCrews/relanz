from django.shortcuts import render
from user.models import User

# Create your views here.

def home(request):
    if request.user.is_anonymous:
         return render(request, 'main/home.html')
    user = User.objects.get(username=request.user)
    return render(request, 'main/home.html')