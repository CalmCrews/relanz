from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from community.models import Article
from django.forms.models import model_to_dict
from django.db.models import Q
import random
from collections import Counter
from datetime import datetime
from django.db.models import Sum, Count


# Create your views here.
def home(request):
    user=request.user
    if user.is_authenticated:
        if not user.is_email_valid:
            return redirect('user:email_sent')
        elif not user.nickname:
            return render(request, 'main/home.html', {'user':user}) 
        participant = Participant.objects.filter(user=user.id)
        try:
            if not participant.exists():
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
                basic_tags = {
                'morning': user_tag.morning,
                'afternoon': user_tag.afternoon,
                'evening': user_tag.evening,
                'inside': user_tag.inside,
                'outside': user_tag.outside,
                'solo': user_tag.solo,
                'group': user_tag.group,
                'pay': user_tag.pay,
                'free': user_tag.free,
                'static': user_tag.static,
                'dynamic': user_tag.dynamic,
                }

                tag_lists=[]
                for tag_name, tag_value in basic_tags.items():
                    if tag_value is True:
                        tag_lists.append(tag_name)

                challenge_query = Q()
                for tag_list in tag_lists:
                    challenge_query |= Q(**{tag_list: True})
                challenges_tags = ChallengeTag.objects.filter(challenge_query)

                
                res_data = survey_result(request)
                res_data2 = {'user':user, 'tag_lists':tag_lists_, 'challenges':challenges_tags}
                res_data.update(res_data2)

                return render(request, 'main/home.html', res_data)
            

            else:
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

                basic_tags = {
                'morning': user_tag.morning,
                'afternoon': user_tag.afternoon,
                'evening': user_tag.evening,
                'inside': user_tag.inside,
                'outside': user_tag.outside,
                'solo': user_tag.solo,
                'group': user_tag.group,
                'pay': user_tag.pay,
                'free': user_tag.free,
                'static': user_tag.static,
                'dynamic': user_tag.dynamic,
                }

                tag_lists=[]
                for tag_name, tag_value in basic_tags.items():
                    if tag_value is True:
                        tag_lists.append(tag_name)
                challenges = ChallengeTag.objects.filter(**{tag_list: True for tag_list in tag_lists})

                # id, user_id 등 불필요한 데이터 제외
                minus_tag = ['id','user']
                for tag_name, tag_value in basic_tags.items():
                    minus_tag.append(tag_name)
                
                # 유저가 릴렌지를 참여함에 따라 빈도 수가 높은 릴렌지 태그를 뽑음
                user_tag_dict = model_to_dict(user_tag)
                for i in range(0, len(minus_tag)):
                    del user_tag_dict[f'{minus_tag[i]}']
                sorted_user_tag = sorted(user_tag_dict.items(), key=lambda x:x[1], reverse=True)
                sorted_user_keys = [item[0] for item in sorted_user_tag]

                # 기본 태그를 통해 가져온 챌린지와 릴렌지 태그를 통해 가져온 챌린지 쿼리를 합집합
                basic_tag_query =Q()
                for key in sorted_user_keys[:4]:
                    basic_tag_query |=Q(**{key: True})
                challenge_tag_query=Q()
                for key in tag_lists:
                    challenge_tag_query |=Q(**{key: True})
                challenge_query = basic_tag_query|challenge_tag_query
                
                challenge_tags = ChallengeTag.objects.filter(challenge_query).order_by(f'-{sorted_user_keys[0]}', f'-{sorted_user_keys[1]}', f'-{sorted_user_keys[2]}', f'-{sorted_user_keys[3]}')
                # 이미 참여한 챌린지는 추천에서 제외
                minus_challenge = []
                # 정렬된 챌린지의 아이디를 뽑아서, requset.user와 challenge.id를 통해 파싱
                for challenge_tag in challenge_tags:
                    already_participant=Participant.objects.filter(challenge=challenge_tag.challenge, user=user.id)
                    # 빈쿼리셋이 반환된 게 아니라면, 이미 참여하고 있는 챌린지 (TRUE)
                    if already_participant.exists():  
                        minus_challenge.append(challenge_tag)
                # x가 sorted_challenge의 element면서 참여하고 있는 챌린지가 아닐 때
                challenge_tags = [x for x in challenge_tags if x not in minus_challenge]

                participants=[]
                for challenge_tag in challenge_tags:
                # 참여자 모델 관련 처리(참여자 쿼리 가져오기, 쿼리 순서 정렬, 정렬된 순서를 바탕으로 쿼리셋 생성)
                    participants.append(Participant.objects.filter(challenge_id=challenge_tag.challenge.id))
                
                sorted_participants = []
                for participant in participants:
                    if participant:
                        sorted_participants.append(participant.values('challenge_id').annotate(count=Count('user_id')).order_by('-count').distinct())
                    else:
                        sorted_participants.append(int(0))
                i = 0
                for sorted_participant in sorted_participants:
                    if sorted_participant != 0:
                        sorted_participants[i] = sorted_participant[0]['count']
                    i+=1
                combined_data = list(zip(challenge_tags, sorted_participants))

                # report 분석 알고리즘
                participant_report = {
                'morning': 0,
                'afternoon': 0,
                'evening': 0,
                'inside': 0,
                'outside': 0,
                'solo': 0,
                'group': 0,
                'pay': 0,
                'free': 0,
                'static': 0,
                'dynamic': 0,
                }
                
                # user_id를 통해 참여자 모델 가져오기
                user_participants = Participant.objects.filter(user=user.id)
                for user_participant in user_participants:
                    analysis_challenge = ChallengeTag.objects.get(challenge=user_participant.challenge_id)
                    for key in participant_report.keys():
                        if getattr(analysis_challenge, key):
                            participant_report[key] += 1

                analysis_user_tag = [k for k, v in sorted(participant_report.items(), key=lambda item: item[1], reverse=True)]
                # 내가 최근 남긴 인증 10개 중에 인증을 가장 많이 남긴 릴렌지 출력
                articles = Article.objects.filter(author__user=user)
                articles = articles.order_by('-created_at')
                if len(articles) > 10:
                    articles=articles[:10]
                like_challenge_list=[]
                for article in articles:
                    like_challenge = article.challenge_id
                    like_challenge_list.append(like_challenge)

                if not like_challenge_list:
                    if len(minus_challenge) == 1:
                        r = 0
                    else:
                        r = random.randint(0, len(minus_challenge)-1)
                    most_like_challenge=minus_challenge[r]
                else:
                    challenge_element = Counter(like_challenge_list)
                    most_common_challenge = challenge_element.most_common(1)[0][0]
                    most_like_challenge = Challenge.objects.get(id=most_common_challenge)

                # 이전에 뽑은 추천할 챌린지 중에 랜덤으로 3개를 픽(중복 제거)
                analysis_challenges = []
                while len(analysis_challenges) < 3:
                    analysis_challenge_tags = random.choice(challenge_tags)
                    if analysis_challenge_tags not in analysis_challenges:
                        analysis_challenges.append(analysis_challenge.challenge)
                analysis_data = {
                    'analysis_user_tag':analysis_user_tag,
                    'most_like_challenge': most_like_challenge,
                    'analysis_titles':analysis_challenges
                }

                res_data = survey_result(request)
                res_data2 = {'user':user, 
                            'tag_lists':tag_lists_, 
                            'combined_data': combined_data, 
                            'analysis_data':analysis_data
                            }
                res_data.update(res_data2)

                return render(request, 'main/home.html', res_data)
            
        except UserTag.DoesNotExist:
            res_data = survey_result(request)
            return redirect('user:survey')
        except (Participant.DoesNotExist, IndexError, ValueError):
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
            basic_tags = {
            'morning': user_tag.morning,
            'afternoon': user_tag.afternoon,
            'evening': user_tag.evening,
            'inside': user_tag.inside,
            'outside': user_tag.outside,
            'solo': user_tag.solo,
            'group': user_tag.group,
            'pay': user_tag.pay,
            'free': user_tag.free,
            'static': user_tag.static,
            'dynamic': user_tag.dynamic,
            }

            tag_lists=[]
            for tag_name, tag_value in basic_tags.items():
                if tag_value is True:
                    tag_lists.append(tag_name)

            challenge_query = Q()
            for tag_list in tag_lists:
                challenge_query |= Q(**{tag_list: True})
            challenges = ChallengeTag.objects.filter(challenge_query)

            res_data = survey_result(request)
            res_data2 = {'user':user, 'tag_lists':tag_lists_, 'challenges':challenges}
            res_data.update(res_data2)

            return render(request, 'main/home.html', res_data)
           
    return render(request, 'main/splashscreen.html')


def survey_result(request):
    user = request.user
    user_survey_result = ''

    # -------------------- 본인 결과 ----------------------
    if user.survey_result_count >= 0 and user.survey_result_count <= 3:
        user_survey_result = '취약하지 않은'
    elif user.survey_result_count >= 4 and user.survey_result_count <= 5:
        user_survey_result = '다소 취약한'
    elif user.survey_result_count >= 6 and user.survey_result_count <= 7:
        user_survey_result = '매우 취약한'

    # -------------------- 전체 기준 -------------------------
    # 순서: '취약하지 않음' - '다소 취약' - '매우 취약'
    all_result_num = [0, 0, 0]

    # 전체 유저 데이터 필터링
    all_users = User.objects.all()

    all_result_num = calculate_result_num(all_users, all_result_num)

    # -------------------- 성별 기준 -------------------------
    sex_result_num = [0, 0, 0]
    user_sex = user.sex

    # 유저와 같은 성별인 데이터 필터링
    sex_group_users = User.objects.filter(
        Q(sex=user_sex)
    )

    sex_result_num = calculate_result_num(sex_group_users, sex_result_num)

    # -------------------- 나이 기준 -------------------------
    age_result_num = [0, 0, 0]
    user_age = user.age

    # 유저 나이대 계산 (유저 나이가 23세면 20~29세)
    age_group_start = (user_age // 10) * 10
    age_group_end = age_group_start + 9

    # 유저와 같은 나이대인 데이터 필터링
    age_group_users = User.objects.filter(
        Q(birth__gt=datetime.now().year - age_group_end, 
            birth__lt=datetime.now().year - age_group_start)
    )

    age_result_num = calculate_result_num(age_group_users, age_result_num)

    # -------------------- 성별+나이 기준 ----------------------
    age_sex_result_num = [0, 0, 0]
            
    # 유저와 같은 성별/나이대인 데이터 필터링 (20대 여성)
    age_sex_group_users = User.objects.filter(
        Q(sex=user_sex, 
            birth__gt=datetime.now().year - age_group_end, 
            birth__lt=datetime.now().year - age_group_start)
    )

    age_sex_result_num = calculate_result_num(age_sex_group_users, age_sex_result_num)
    avg_result = calculate_avg_result(user, age_sex_group_users)

    # --------------- 인원수를 퍼센트로 계산 ----------------
    total_all_users = all_users.count()
    total_sex_users = sex_group_users.count()
    total_age_users = age_group_users.count()
    total_age_sex_users = age_sex_group_users.count()

    all_percentages = []
    sex_percentages = []
    age_percentages = []
    age_sex_percentages = []

    if total_all_users != 0:
        all_percentages = [round((value / total_all_users) * 100) for value in all_result_num]

    if total_sex_users != 0:
        sex_percentages = [round((value / total_sex_users) * 100) for value in sex_result_num]

    if total_age_users != 0:
        age_percentages = [round((value / total_age_users) * 100) for value in age_result_num]

    if total_age_sex_users != 0:
        age_sex_percentages = [round((value / total_age_sex_users) * 100) for value in age_sex_result_num]

    res_data = {'user_survey_result':user_survey_result,
                'age_group_start':age_group_start,
                'all_percentages':all_percentages, 
                'sex_percentages':sex_percentages,
                'age_percentages':age_percentages,
                'age_sex_percentages':age_sex_percentages,
                'avg_result':avg_result}
    return res_data

def calculate_result_num(users, result_num):
    for u in users:
        if u.survey_result_count >= 0 and u.survey_result_count <= 3:
            result_num[0] += 1
        elif u.survey_result_count >= 4 and u.survey_result_count <= 5:
            result_num[1] += 1
        elif u.survey_result_count >= 6 and u.survey_result_count <= 7:
            result_num[2] += 1
    return result_num

# 스트레스 취약성 평균인지 아닌지 계산
def calculate_avg_result(user, users):
    total = 0
    count = 0
    for u in users:
        total += u.survey_result_count
        count += 1

    if count > 0:
        average = total / count
        if user.survey_result_count > average:
            result = '평균 이상'
        elif user.survey_result_count < average:
            result = '평균 이하'
        else:
            result = '평균적'
    else:
        result = '데이터 없음'
    
    return result