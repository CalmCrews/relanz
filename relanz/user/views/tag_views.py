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
        if request.user.is_authenticated:
            # -------------------- 전체 기준 -------------------------
            all_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0,
            }

            # 전체 유저 데이터 필터링
            all_users = User.objects.all()

            for user in all_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    all_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    all_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    all_result_num['매우 취약'] += 1

            # -------------------- 성별 기준 -------------------------
            sex_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0,
            }
            user_sex = user.sex

            # 유저와 같은 성별인 데이터 필터링
            sex_group_users = User.objects.filter(
                Q(sex=user_sex)
            )

            for user in sex_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    sex_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    sex_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    sex_result_num['매우 취약'] += 1

            # -------------------- 나이 기준 -------------------------
            age_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0
            }
            user_age = user.age

            # 유저 나이대 계산 (유저 나이가 23세면 20~29세)
            age_group_start = (user_age // 10) * 10
            age_group_end = age_group_start + 9

            # 유저와 같은 나이대인 데이터 필터링
            age_group_users = User.objects.filter(
                Q(birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for user in age_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    age_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    age_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    age_result_num['매우 취약'] += 1

            # -------------------- 성별+나이 기준 ----------------------
            age_sex_result_num = {
                '취약하지 않음': 0,
                '취약': 0,
                '매우 취약': 0
            }
            
            # 유저와 같은 성별/나이대인 데이터 필터링 (20대 여성)
            age_sex_group_users = User.objects.filter(
                Q(sex=user_sex, 
                  birth__gt=datetime.now().year - age_group_end, 
                  birth__lt=datetime.now().year - age_group_start)
            )

            for user in age_sex_group_users:
                if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                    age_sex_result_num['취약하지 않음'] += 1
                elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                    age_sex_result_num['취약'] += 1
                elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                    age_sex_result_num['매우 취약'] += 1
            

            # 인원수를 퍼센트로 계산
            total_all_users = all_users.count()
            total_sex_users = sex_group_users.count()
            total_age_users = age_group_users.count()
            total_age_sex_users = age_sex_group_users.count()

            all_percentages = {key: round((value / total_all_users) * 100) for key, value in all_result_num.items()}
            sex_percentages = {key: round((value / total_sex_users) * 100) for key, value in sex_result_num.items()}
            age_percentages = {key: round((value / total_age_users) * 100) for key, value in age_result_num.items()}
            age_sex_percentages = {key: round((value / total_age_sex_users) * 100) for key, value in age_sex_result_num.items()}

            # -------------------- 본인 결과 ----------------------
            if user.survey_result_count >= 1 and user.survey_result_count <= 3:
                user_survey_result = '취약하지 않음'
            elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
                user_survey_result = '취약'
            elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
                user_survey_result = '매우 취약'
            
            return redirect('user:tagsurvey')
        
    res_data = {'all_percentages':all_percentages, 
                'sex_percentages':sex_percentages, 
                'age_percentage':age_percentages, 
                'age_sex_percentages':age_sex_percentages,
                'user_survey_result':user_survey_result}
    return render(request, 'main/home.html', res_data)

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
        group = request.POST.get('Group')
        static = request.POST.get('static')
        dynamic = request.POST.get('dynamic')
        anytime = request.POST.get('anytime')
        tag_cnt = 0
        tag_lists = [morning, afternoon, evening, inside, outside, solo, group, static, dynamic, anytime]
        for tag_list in tag_lists:
            if tag_list is not None:
                tag_cnt += 1
        if tag_cnt > 0:
            if morning is not None:
                tags.morning = True
            else:
                tags.morning =False

            if afternoon is not None:
                tags.afternoon = True
            else:
                tags.afternoon =False

            if evening is not None:
                tags.evening = True
            else:
                tags.evening =False

            if inside is not None:
                tags.inside = True
            else:
                tags.inside =False

            if outside is not None:
                tags.outside = True
            else:
                tags.outside =False

            if solo is not None:
                tags.solo = True
            else:
                tags.solo =False

            if group is not None:
                tags.group = True
            else:
                tags.group =False

            if static is not None:
                tags.static = True
            else:
                tags.static =False

            if dynamic is not None:
                tags.dynamic = True
            else:
                tags.dynamic =False

            if anytime is not None:
                tags.morning = True
                tags.afternoon = True
                tags.evening = True
            tags.save()
            if user.avatar is None:
                return redirect('user:avatar')
            else:
                return redirect('user:userinfo', user.id)
        else:
            messages.add_message(request, messages.ERROR, '')
            return render(request, 'tag/tagsurvey.html')
    return render(request, 'main/home.html')