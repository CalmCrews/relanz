from django.shortcuts import render, redirect, get_object_or_404
from ..models import Tag
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
            return redirect('user:avatar')
        else:
            messages.add_message(request, messages.ERROR, '하나 이상 선택해 주세요.')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')