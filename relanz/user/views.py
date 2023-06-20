from django.shortcuts import render, redirect
from .models import User
from account.models import Account
from django.contrib.auth import login, logout, authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


# Create your views here.

@csrf_protect
def signup(request):
    if request.method=="GET":
        return render(request, 'user/signup.html')
    elif request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['re_password']
        res_data = {'username':username, 'password':password}
        if not (username and password and re_password):
            res_data['error']="입력되지 않은 값이 있습니다."
            render(request, 'user/signup.html', res_data)
        elif (password != re_password):
            res_data['error']="비밀번호가 일치하지 않습니다."
            render(request, 'user/signup.html', res_data)
        else:
            user=User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()
            return redirect('user:signin')

@csrf_protect
def identify(request):
        json_data=json.loads(request.body)
        username = json_data.get('id')
        if User.objects.filter(username=username).exists():
            message = {'message': '이미 있는 아이디입니다.'}
            return JsonResponse(message, status=200)
        return render(request, 'user/signup.html')
        
        
def signin(request):
    if request.method == "GET":
        return render(request,'user/signin.html')
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                return render(request, 'user/signin.html', {'error':"아이디 혹은 비밀번호가 다릅니다."})
        else:
            return redirect('main:home')
        
def signout(request):
    logout(request)
    return render(request, 'user/signout.html')
