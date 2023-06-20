from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.

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
            return render(request, 'user/signup.html', res_data)
        elif (password != re_password):
            res_data['error']="비밀번호가 일치하지 않습니다."
            return render(request, 'user/signup.html', res_data)
        elif User.objects.filter(username=username):
            res_data['error']="이미 존재하는 아이디입니다."
            return render(request, 'user/signup.html', res_data)
        else:
            user=User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()
            return redirect('user:signin')
        
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




def nickname(request):
    user_data={}
    if request.method=="GET":
        return render(request, 'user/nickname.html')
    if request.method=="POST":
        nickname = request.POST.get('nickname')
        user = User.objects.get(username=request.user)
        if not nickname:
            user_data['error'] = "닉네임을 입력해주세요."
            return render(request, 'user/nickname.html', user_data)
        
        elif User.objects.filter(nickname=nickname).exists():
            user_data['error'] = "이미 존재하는 닉네임입니다."
            return render(request, 'user/nickname.html', user_data)
        else:
            user.nickname = nickname
            user.save()
            return redirect('user:content')



def content(request):
    if request.method=="GET":
        return render(request, 'user/content.html')
    if request.method=="POST":
        user = User.objects.get(username=request.user)
        birth = request.POST.get('birth')
        sex = request.POST.get('sex')
        user.birth = birth
        user.sex = sex
        user.save()
        return redirect('user:userinfo', user.id)
    

def userinfo(request, user_id):
    user = User.objects.get(username=request.user)
    user.birth = 2023 - user.birth
    return render(request, 'user/userinfo.html', {'user':user})
