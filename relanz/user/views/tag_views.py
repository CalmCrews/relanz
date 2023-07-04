from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, UserTag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from config.email_decorator import email_verified_required

# @email_verified_required
@login_required(login_url='/user/signin')
def survey(request):
    if request.method=="GET":
        user = request.user
        print(user)
        print(user.nickname)
        return render(request, 'tag/survey.html', {"user":user.nickname})
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        if user.is_authenticated:
            user.survey_result_count = int(request.POST.get('survey_result_count'))
            user.save()
        return redirect('user:tagsurvey')
    return render(request, 'main/home.html')

# @email_verified_required
@login_required(login_url='/user/signin')
def tagsurvey(request):
    user=request.user
    if request.method=="GET":
        try:
            tags = UserTag.objects.get(user=user)
        except UserTag.DoesNotExist:
            tags = UserTag.objects.create(user=user)
        return render(request, 'tag/tagsurvey.html', {'tags':tags})
    if request.method=="POST":
        if user.nickname is None:
            return redirect('user:content')
        tags = UserTag.objects.get(user=user)
        morning = request.POST.get('morning')
        afternoon = request.POST.get('afternoon')
        evening = request.POST.get('evening')
        inside = request.POST.get('inside')
        outside = request.POST.get('outside')
        solo = request.POST.get('solo')
        group = request.POST.get('group')
        static = request.POST.get('static')
        dynamic = request.POST.get('dynamic')
        anytime = request.POST.get('anytime')
        tag_cnt = 0
        tag_lists = [morning, afternoon, evening, inside, outside, solo, group, static, dynamic, anytime]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if morning == 'morning':
                tags.morning = True
            else:
                tags.morning =False

            if afternoon == 'afternoon':
                tags.afternoon = True
            else:
                tags.afternoon =False

            if evening == 'evening':
                tags.evening = True
            else:
                tags.evening =False

            if inside == 'inside':
                tags.inside = True
            else:
                tags.inside =False

            if outside == 'outside':
                tags.outside = True
            else:
                tags.outside =False

            if solo == 'solo':
                tags.solo = True
            else:
                tags.solo =False

            if group == 'group':
                tags.group = True
            else:
                tags.group =False

            if static == 'static':
                tags.static = True
            else:
                tags.static =False

            if dynamic == 'dynamic':
                tags.dynamic = True
            else:
                tags.dynamic =False

            if anytime == 'anytime':
                tags.morning = True
                tags.afternoon = True
                tags.evening = True
            tags.save()
            if user.avatar is None:
                return redirect('user:avatar')
            else:
                return redirect('user:userinfo')
        else:
            messages.add_message(request, messages.ERROR, '')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html', {user:user})