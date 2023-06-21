from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import login, logout, authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required



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

@login_required(login_url='/user/signin')
def content(request):
    if request.method=="GET":
        return render(request, 'user/content.html')
    if request.method=="POST":
        message = {}
        user = request.user
        user = User.objects.get(username=user.username)

        nickname = request.POST.get('nickname')
        birth = request.POST.get('birth')
        sex = request.POST.get('sex')
        if not nickname:
            message['error'] = "닉네임을 입력해주세요."
            return render(request, 'user/content.html', message)
        elif User.objects.filter(nickname=nickname).exists():
            message['error'] = "이미 존재하는 닉네임입니다."
            return render(request, 'user/content.html', message)
        else:
            user.nickname = nickname
            user.birth = birth
            user.sex = sex
            user.save()
            return redirect('user:survey')
    

@login_required(login_url='/user/signin')
def survey(request):
    if request.method=="GET":
        return render(request, 'tag/survey.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return render(request, 'user/content.html', {'user':user})
        if request.user.is_authenticated:
            return redirect('user:survey')
    return render(request, 'main/home.html')





@login_required(login_url='/user/signin')
def userinfo(request, user_id):
    user = request.user
    user = User.objects.get(username=user.username) 
    return render(request, 'user/userinfo.html', {'user':user})

# views.py에 함수가 너무 많고 길어져서 https://wikidocs.net/71657#pybourlspy를 참고해서 바꾸는 게 좋을 듯 합니다.
# user와 profile로 나누는 게 가장 적당하고 생각합니다. 그래도 길면은 survey, profile, user이렇게 3개...

# def accountedit(request, user_id):
#     account = get_object_or_404(User, pk=user_id)
#     if request.method == 'GET':
#         return render(request, 'user/accountedit.html', {'user':account})
#     if request.method == 'POST':
#         message = {}
#         nickname = request.POST.get('nickname')
#         birth = request.POST.get('birth')
#         sex = request.POST.get('sex')
#         if not nickname:
#             message['error'] = "닉네임을 입력해주세요."
#             return render(request, 'user/accountedit.html', message)
#         elif User.objects.filter(nickname=nickname).exists():
#             if account.nickname == nickname:
#                     account.nickname = nickname
#                     account.birth = birth 
#                     account.sex = sex
#                     account.save()
#                     return redirect('user:userinfo', account.id)
            
#             message['error'] = "이미 존재하는 닉네임입니다."
#             return render(request, 'user/accountedit.html', message)
#         else:
#             account.nickname = nickname
#             account.birth = birth 
#             account.sex = sex
#             account.save()
#             return redirect('user:userinfo', account.id)