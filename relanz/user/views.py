from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Tag   
from django.contrib.auth import login, logout, authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth.decorators import login_required
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
    return render(request, 'main/home.html')

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
            return redirect('user:content')
        if request.user.is_authenticated:
            return redirect('user:release')
    return render(request, 'main/home.html')

@login_required(login_url='/user/signin')
def release(request):
    if request.method=="GET":
        return render(request, 'tag/release.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        if request.user.is_authenticated:
            return redirect('user:activetime')
    return render(request, 'main/home.html')


@login_required(login_url='/user/signin')
def activetime(request):
    if request.method=="GET":
        return render(request, 'tag/activetime.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        morning = request.POST.get('morning')
        afternoon = request.POST.get('afternoon')
        evening = request.POST.get('evening')
        if morning or afternoon or evening:
            try:
                tags = Tag.objects.get(user=user)
            except Tag.DoesNotExist:
                tags = Tag.objects.create(user=user)
            if morning is not None:
                tags.morning = True
            if afternoon is not None:
                tags.afternoon = True
            if evening is not None:
                tags.evening = True
            tags.save()
            return redirect('user:tagsurvey')
        else:
            messages.add_message(request, messages.ERROR, '하나 이상 선택해 주세요.')
            return render(request, 'tag/activetime.html')
    return render(request, 'main/home.html')

@login_required(login_url='/user/signin')
def tagsurvey(request):
    if request.method=="GET":
        return render(request, 'tag/tagsurvey.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        try:
            tags = Tag.objects.get(user=user)
        except Tag.DoesNotExist:
            tags = Tag.objects.create(user=user)
            return redirect('user:activetime')
        
        inside = request.POST.get('inside')
        outside = request.POST.get('outside')
        solo = request.POST.get('solo')
        group = request.POST.get('group')
        extreme = request.POST.get('extreme')
        calm = request.POST.get('calm')
        focus = request.POST.get('focus')
        achievement = request.POST.get('achievement')
        bodyhealth = request.POST.get('bodyhealth')
        confidence = request.POST.get('confidence')
        mental = request.POST.get('mental')
        short = request.POST.get('short')
        newtry = request.POST.get('newtry')
        tags = Tag.objects.get(user=user)
        tag_cnt = 0
        tag_lists = [inside, outside, solo, group, extreme, calm, focus, achievement, bodyhealth, confidence, mental, short, newtry]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if inside is not None:
                tags.inside = True
            if outside is not None:
                tags.outside = True
            if extreme is not None:
                tags.extreme = True
            if calm is not None:
                tags.calm = True
            if focus is not None:
                tags.focus = True
            if achievement is not None:
                tags.achievement = True
            if bodyhealth is not None:
                tags.bodyhealth = True
            if confidence is not None:
                tags.confidence = True
            if mental is not None:
                tags.mental = True
            if short is not None:
                tags.short = True
            if newtry is not None:
                tags.newtry = True
            tags.save()
            return redirect('user:userinfo', user.id)
        else:
            messages.add_message(request, messages.ERROR, '하나 이상 선택해 주세요.')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')



@login_required(login_url='/user/signin')
def userinfo(request, user_id):
    user = request.user
    user = User.objects.get(username=user.username) 
    tags = Tag.objects.get(user_id=user_id)
    
    
    return render(request, 'user/userinfo.html', {'user':user, 'tags':tags})

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