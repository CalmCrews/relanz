from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from config.email_decorator import email_verified_required
from user.models import User, UserTag
from challenge.models import Challenge, Participant

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
        elif user.nickname is not None or user.nickname == nickname:
            user.nickname = nickname
            user.birth = birth
            user.sex = sex
            user.save()
            return redirect('user:userinfo', user.id)
        else:
            if User.objects.filter(nickname=nickname).exists():
                message['error'] = "이미 존재하는 닉네임입니다."
                return render(request, 'user/content.html', message)
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
    user_tag = UserTag.objects.get(user=user.id)
    basic_tags_ = {
        '아침': user_tag.morning,
        '점심': user_tag.afternoon,
        '저녁': user_tag.evening,
        '실내': user_tag.inside,
        '야외': user_tag.outside,
        '혼자': user_tag.solo,
        '여럿이': user_tag.group,
        '정적인': user_tag.static,
        '동적인': user_tag.dynamic,
        }
    tag_lists_=[]
    for tag_name, tag_value in basic_tags_.items():
        if tag_value is True:
            tag_lists_.append(tag_name)

    participants = Participant.objects.filter(user=user.id)
    challenges=[]
    for participant in participants:
        challenges.append(participant.challenge)
        
    res_data = {'user':user, 'tags':tag_lists_, 'challenges':challenges}
    
    return render(request, 'user/userinfo.html', res_data)

    
    
