from django.shortcuts import render, redirect, get_object_or_404
from ..models import UserTag
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
                tags = UserTag.objects.get(user=user)
            except UserTag.DoesNotExist:
                tags = UserTag.objects.create(user=user)
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
            tags = UserTag.objects.get(user=user)
        except UserTag.DoesNotExist:
            tags = UserTag.objects.create(user=user)
            return redirect('user:activetime')
        inside = request.POST.get('inside')
        outside = request.POST.get('outside')
        solo = request.POST.get('solo')
        group = request.POST.get('Group')
        pay = request.POST.get('pay')
        free = request.POST.get('free')
        static = request.POST.get('static')
        dynamic = request.POST.get('dynamic')
        tags = UserTag.objects.get(user=user)
        tag_cnt = 0
        tag_lists = [inside, outside, solo, group, pay, free, static, dynamic]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if inside is not None:
                tags.inside = True
            if outside is not None:
                tags.outside = True
            if solo is not None:
                tags.solo = True
            if group is not None:
                tags.group = True
            if pay is not None:
                tags.pay = True
            if free is not None:
                tags.static = True
            if dynamic is not None:
                tags.dynamic = True
            tags.save()
            return redirect('user:avatar')
        else:
            messages.add_message(request, messages.ERROR, '하나 이상 선택해 주세요.')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')