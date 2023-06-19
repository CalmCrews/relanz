from django.shortcuts import render
from user.models import User
from account.models import Account

# Create your views here.

def home(request):
    if request.user.is_anonymous:
         return render(request, 'main/home.html')
    user = User.objects.get(username=request.user)
    if Account.objects.filter(user=request.user).exists():
        account = Account.objects.get(user_id=user.id)
        return render(request, 'main/home.html', {'account':account})
    return render(request, 'main/home.html')

def login(request):
    return render(request, 'user/signin.html')