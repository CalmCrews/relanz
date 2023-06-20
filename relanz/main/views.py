from django.shortcuts import render
from user.models import User
from account.models import Account

# Create your views here.

def home(request):
    if request.user.is_anonymous:
         return render(request, 'main/home.html')
    user = User.objects.get(username=request.user)
    if User.objects.filter(user=request.user).exists():
        account = User.objects.get(user_id=user.id)
        return render(request, 'main/home.html', {'account':account})
    return render(request, 'main/home.html')

# 이인이 signin.html 연결해볼라고 임시로 만듬
# def login(request):
    # return render(request, 'user/signin.html') 
# 주석처리할게요