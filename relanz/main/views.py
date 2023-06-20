from django.shortcuts import render
from user.models import User

# Create your views here.

def home(request):
    if request.user.is_anonymous:
         return render(request, 'main/home.html')

    user = request.user
    if User.objects.filter(username=user.username).exists():
        user = User.objects.get(username=user)
        return render(request, 'main/home.html', {'user':user})
    return render(request, 'main/home.html')


