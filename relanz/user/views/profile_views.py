from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, UserTag
from django.contrib.auth.decorators import login_required
from config.email_decorator import email_verified_required

@login_required(login_url='/user/signin')
@email_verified_required
def content(request):
    if request.method=="GET":
        user = User.objects.get(id=request.user.id)
        return render(request, 'user/content.html', {'user':user})
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
        elif user.nickname is not None and user.nickname == nickname:
            user.nickname = nickname
            user.birth = birth
            user.sex = sex
            user.save()
            return redirect('user:userinfo',user.id)
        else:
            user.nickname = nickname
            user.birth = birth
            user.sex = sex
            user.save()
            return redirect('user:survey')
        
@login_required(login_url='/user/signin') 
def avatar(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        return render(request, 'user/avatar.html')
    if request.method == 'POST':
        user = request.user
        if user.avatar is None:
            user.avatar = request.POST.get('avatar')
            user.save()
            return redirect('main:home')
        user.avatar = request.POST.get('avatar')
        user.save()
        return redirect('user:userinfo', user.id)
    
@login_required(login_url='/user/signin')
def userinfo(request, user_id):
    user = request.user
    user = User.objects.get(username=user.username) 
    tags = UserTag.objects.get(user_id=user_id)

    res_data = {'user':user, 'tags':tags}
    
    return render(request, 'user/userinfo.html', res_data)

    
    
