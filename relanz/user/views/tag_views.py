from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, UserTag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from config.email_decorator import email_verified_required
from django.db.models import Q
from datetime import datetime

# @email_verified_required
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
            user.survey_result_count = int(request.POST.get('survey_result_count'))
            user.save()
            # -------------------- 전체 기준 -------------------------
            # 순서: '취약하지 않음' - '취약' - '매우 취약'
            all_result_num = [0, 0, 0]

            # 전체 유저 데이터 필터링
            all_users = User.objects.all()

            for u in all_users:
                if u.survey_result_count >= 1 and u.survey_result_count <= 3:
                    all_result_num[0] += 1
                elif u.survey_result_count >= 4 and u.survey_result_count <= 5:
                    all_result_num[1] += 1
                elif u.survey_result_count >= 6 and u.survey_result_count <= 7:
                    all_result_num[2] += 1

            # -------------------- 성별 기준 -------------------------
            sex_result_num = [0, 0, 0]
            user_sex = user.sex

            # 유저와 같은 성별인 데이터 필터링
            sex_group_users = User.objects.filter(
                Q(sex=user_sex)
            )

            for u in sex_group_users:
                if u.survey_result_count >= 1 and u.survey_result_count <= 3:
                    sex_result_num[0] += 1
                elif u.survey_result_count >= 4 and u.survey_result_count <= 5:
                    sex_result_num[1] += 1
                elif u.survey_result_count >= 6 and u.survey_result_count <= 7:
                    sex_result_num[2] += 1

            # -------------------- 나이 기준 -------------------------
            age_result_num = [0, 0, 0]
            user_age = user.age

            # 유저 나이대 계산 (유저 나이가 23세면 20~29세)
            age_group_start = (user_age // 10) * 10
            age_group_end = age_group_start + 9

            request.session['age_group_start'] = age_group_start

            print(age_group_start)

            # 유저와 같은 나이대인 데이터 필터링
            age_group_users = User.objects.filter(
                Q(birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for u in age_group_users:
                if u.survey_result_count >= 1 and u.survey_result_count <= 3:
                    age_result_num[0] += 1
                elif u.survey_result_count >= 4 and u.survey_result_count <= 5:
                    age_result_num[1] += 1
                elif u.survey_result_count >= 6 and u.survey_result_count <= 7:
                    age_result_num[2] += 1

            # -------------------- 성별+나이 기준 ----------------------
            age_sex_result_num = [0, 0, 0]
            
            # 유저와 같은 성별/나이대인 데이터 필터링 (20대 여성)
            age_sex_group_users = User.objects.filter(
                Q(sex=user_sex, 
                  birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for u in age_sex_group_users:
                if u.survey_result_count >= 1 and u.survey_result_count <= 3:
                    age_sex_result_num[0] += 1
                elif u.survey_result_count >= 4 and u.survey_result_count <= 5:
                    age_sex_result_num[1] += 1
                elif u.survey_result_count >= 6 and u.survey_result_count <= 7:
                    age_sex_result_num[2] += 1
            
            # --------------- 인원수를 퍼센트로 계산 ----------------
            total_all_users = all_users.count()
            total_sex_users = sex_group_users.count()
            total_age_users = age_group_users.count()
            total_age_sex_users = age_sex_group_users.count()

            all_percentages = [round((value / total_all_users) * 100) for value in all_result_num]
            sex_percentages = [round((value / total_sex_users) * 100) for value in sex_result_num]
            age_percentages = [round((value / total_age_users) * 100) for value in age_result_num]
            age_sex_percentages = [round((value / total_age_sex_users) * 100) for value in age_sex_result_num]

            # -------------------- 본인 결과 ----------------------
            if user.survey_result_count >= 0 and user.survey_result_count <= 3:
                user_survey_result = '취약하지 않음'
            elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                user_survey_result = '취약'
            elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                user_survey_result = '매우 취약'

            request.session['all_survey_result'] = all_percentages
            request.session['sex_survey_result'] = sex_percentages
            request.session['age_survey_result'] = age_percentages
            request.session['age_sex_survey_result'] = age_sex_percentages
            request.session['user_survey_result'] = user_survey_result

            return redirect('user:tagsurvey')
        
    return render(request, 'main/home.html')

# @email_verified_required
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