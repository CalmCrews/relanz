from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from ..models import User
from django.contrib.auth import login, logout, authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages

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

@csrf_exempt
def identify(request):
        json_data=json.loads(request.body)
        username = json_data.get('id')
        if User.objects.filter(username=username).exists():
            message = {'message': '이미 있는 아이디입니다.'}
            return JsonResponse(message, status=400)
        return render(request, 'user/signup.html')

def signin(request):
    if request.method == "GET":
        return render(request,'user/signin.html')
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            if not username:
                messages.add_message(request, messages.ERROR, 'Please enter a valid username.')
                return render(request, 'user/signin.html')
            if not password:
                messages.add_message(request, messages.ERROR, 'Please enter a valid password.')
                return render(request, 'user/signin.html')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                messages.add_message(request, messages.ERROR, '유효한 ID와 비밀번호가 아닙니다.')
                return render(request, 'user/signin.html')
        else:
            return redirect('main:home')
                
def signout(request):
    logout(request)
    return redirect('main:home')