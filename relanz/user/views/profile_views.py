from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, UserTag
from django.contrib.auth.decorators import login_required

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
def avatar(request):
    if request.method == 'GET':
        return render(request, 'user/avatar.html')
    if request.method == 'POST':
        user = request.user
        user.avatar = request.POST.get('avatar')
        user.save()
        return redirect('main:home')
    
@login_required(login_url='/user/signin')
def userinfo(request, user_id):
    user = request.user
    user = User.objects.get(username=user.username) 
    tags = UserTag.objects.get(user_id=user_id)

    res_data = {'user':user, 'tags':tags}
    
    return render(request, 'user/userinfo.html', res_data)

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


