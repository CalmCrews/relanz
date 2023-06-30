from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from community.models import Article
from django.forms.models import model_to_dict
from django.db.models import Q
import random
from collections import Counter

# Create your views here.
def home(request):
    user=request.user
    if user.is_authenticated:
        if not user.is_email_valid:
            # return redirect('user:email_sent')
            return redirect('user:email_sent')
        elif not user.nickname:
            return render(request, 'main/home.html', {'user': user})
        try:
            user_tag = UserTag.objects.get(user=user.id)
            participant = Participant.objects.get(user=user.id)
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
            challenge_ids  = challenge_tags.values_list('challenge', flat=True)
            challenges = Challenge.objects.filter(id__in=challenge_ids)
            challenge_order = {challenge_id: order for order, challenge_id in enumerate(challenge_ids)}
            sorted_challenges = sorted(challenges, key=lambda c: challenge_order.get(c.id, float('inf')))
            # 이미 참여한 챌린지는 추천에서 제외
            minus_challenge = []
            # 정렬된 챌린지의 아이디를 뽑아서, requset.user와 challenge.id를 통해 파싱
            for sorted_challenge in sorted_challenges:
                already_participant=Participant.objects.filter(challenge=sorted_challenge.id, user=user.id)
                # 빈쿼리셋이 반환된 게 아니라면, 이미 참여하고 있는 챌린지 (TRUE)
                if already_participant.exists():  
                    minus_challenge.append(sorted_challenge)
            # x가 sorted_challenge의 element면서 참여하고 있는 챌린지가 아닐 때
            sorted_challenges = [x for x in sorted_challenges if x not in minus_challenge]

            # 참여자 모델 관련 처리(참여자 쿼리 가져오기, 쿼리 순서 정렬, 정렬된 순서를 바탕으로 쿼리셋 생성)
            participants = Participant.objects.filter(challenge_id__in=sorted_challenges)
            participants_order = {challenge_id: order for order, challenge_id in enumerate(challenge_ids)}
            sorted_participants = sorted(participants, key=lambda p: participants_order.get(p.challenge_id, float('inf')))
            # 챌린지 아이디 순서를 기준으로 참여자 tuple 순서를 반환
            participant_ids = [p.challenge_id for p in sorted_participants]
            # 반환 튜플의 순서 리스트에서 각 리스트에서 중복되는 값을 제외 
            unique_numbers = list(dict.fromkeys(participant_ids))
            # 중복되는 값을 제외한 튜플에서 count를 통해 각 챌린지 당 참여자의 수를 반환
            participant_counts = [participants.filter(challenge_id=unique_number).count() for unique_number in unique_numbers]

            # 챌린지와 참여자의 수를 튜플로 묶어서 전달
            combined_data = list(zip(sorted_challenges, participant_counts))

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
            analysis_titles = []
            while len(analysis_titles) < 3:
                analysis_title = random.choice(sorted_challenges)
                if analysis_title.title not in analysis_titles:
                    analysis_titles.append(analysis_title.title)

            analysis_data = {
                'analysis_user_tag':analysis_user_tag,
                'most_like_challenge': most_like_challenge,
                'analysis_titles':analysis_titles
            }
            # ------------ survey 결과 가져오기 --------------
            age_group_start = request.session.get('age_group_start')
            all_survey_result = request.session.get('all_survey_result')
            sex_survey_result = request.session.get('sex_survey_result')
            age_survey_result = request.session.get('age_survey_result')
            age_sex_survey_result = request.session.get('age_sex_survey_result')
            user_survey_result = request.session.get('user_survey_result')


            # -------------------------------------------------

            res_data = {'user':user, 
                        'tag_lists':tag_lists_, 
                        'combined_data': combined_data, 
                        'age_group_start':age_group_start,
                        'all_survey_result':all_survey_result, 
                        'sex_survey_result':sex_survey_result,
                        'age_survey_result':age_survey_result,
                        'age_sex_survey_result':age_sex_survey_result,
                        'user_survey_result':user_survey_result,
                        'analysis_data':analysis_data
                        }
            return render(request, 'main/home.html', res_data)
        except UserTag.DoesNotExist:
            return redirect('user:tagsurvey')
        except Participant.DoesNotExist:
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
            return render(request, 'main/home.html', {'user':user, 'tag_lists':tag_lists_, 'challengs':challenges})
        
            
    return render(request, 'main/splashscreen.html')