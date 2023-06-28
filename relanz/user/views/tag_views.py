from django.shortcuts import render, redirect, get_object_or_404
from ..models import UserTag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from config.email_decorator import email_verified_required

@email_verified_required
@login_required(login_url='/user/signin')
def survey(request):
    if request.method=="GET":
        user = request.user
        return render(request, 'tag/survey.html', {user:user})
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        if user.is_authenticated:
            # # 전체
            # # if survey_result_count >= 1 and survey_result_count <=3
            # # 1-3 취약하지 않음
            # survey_result_count
            # # 4-5 취약
            # # 6-7 매우 취약

            # # 성별
            
            # User.objects.filter(sex='sex')

            # # 나이

            # User.objects
            
            # # 성별+나이

            # age = user.age
            # sex = user.sex
            return redirect('user:tagsurvey')
    return render(request, 'main/home.html')

@email_verified_required
@login_required(login_url='/user/signin')
def tagsurvey(request):
    if request.method=="GET":
        return render(request, 'tag/tagsurvey.html')
    if request.method=="POST":
        user=request.user
        if user.nickname is None:
            return redirect('user:content')
        try:
            tags = UserTag.objects.get(user=user)
        except UserTag.DoesNotExist:
            tags = UserTag.objects.create(user=user)
            return redirect('user:activetime')
        morning = request.POST.get('morning')
        afternoon = request.POST.get('afternoon')
        evening = request.POST.get('evening')
        inside = request.POST.get('inside')
        outside = request.POST.get('outside')
        solo = request.POST.get('solo')
        group = request.POST.get('Group')
        static = request.POST.get('static')
        dynamic = request.POST.get('dynamic')
        tags = UserTag.objects.get(user=user)
        tag_cnt = 0
        tag_lists = [morning, afternoon, evening, inside, outside, solo, group, static, dynamic]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if morning is not None:
                tags.morning = True
            if afternoon is not None:
                tags.afternoon = True
            if evening is not None:
                tags.evening = True
            if inside is not None:
                tags.inside = True
            if outside is not None:
                tags.outside = True
            if solo is not None:
                tags.solo = True
            if group is not None:
                tags.group = True
            if static is not None:
                tags.static = True
            if dynamic is not None:
                tags.dynamic = True
            tags.save()
            return redirect('user:avatar')
        else:
            messages.add_message(request, messages.ERROR, '')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')