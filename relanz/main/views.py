from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from django.forms.models import model_to_dict
from django.db.models import Q

from community.models import Article
from django.db.models import Sum, Count
from datetime import datetime


# Create your views here.
def home(request):
    user=request.user
    if user.is_authenticated:
        if not user.is_email_valid:
            return redirect('user:email_sent')
        try:
            user_tag = UserTag.objects.get(user=user.id)
            participant = Participant.objects.filter(user=user.id)
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

            return render(request, 'main/home.html', {'user':user, 'tag_lists':tag_lists_, 'combined_data': combined_data})
        except UserTag.DoesNotExist:
            user_tag = UserTag.objects.create(user=user)
            return render(request, 'main/home.html', {'user':user})
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



def ranking(request, user_id):
    # 내가 속한 챌린지의 랭킹
    user=request.user
    participants = Participant.objects.filter(user=user)

    # 내가 참여하고 있는 챌린지 리스트
    challenges = []
    for participant in participants:
        challenge = participant.challenge
        challenges.append(challenge)

    # 내가 쓴 글의 쿼리셋
    articles = Article.objects.filter(author__in=participants)

    # 내가 쓴 글의 쿼리셋을 challenge를 기준으로 묶어서, score를 기준으로 정렬
    ranked_articles = articles.values('challenge').annotate(sum=Sum('article_score')).distinct()
    ranked_articles = ranked_articles.order_by('-sum')
    
    # 정렬한 쿼리셋을 기준으로 챌린지 객체를 list 형식으로 인덱스 = 순위가 될 수 있도록 추가
    ranked_my_challenges = []
    for ranked_article in ranked_articles[:3]:
        ranked_my_challenge = Challenge.objects.get(id=ranked_article['challenge'])
        ranked_my_challenges.append(ranked_my_challenge)

    # TOP3의 챌린지 중에 내 순위
    rank = []
    # TOP 1,TOP 2, TOP 3 챌린지에 해당하는 글 모으기
    for my_rank in ranked_my_challenges:
        article_list = Article.objects.filter(challenge=my_rank)

        # user.id를 기준으로 중복없이 group by, 합쳐진 score를 기준으로 정렬
        user_rank = article_list.values('author__user').annotate(sum=Sum('article_score')).distinct()
        user_rank = user_rank.order_by('-sum')

        # list에 순위를 기준으로 차례대로 list에 추가
        user_rank_list = list(user_rank)

        # list의 인덱스 번호를 토대로 순위를 tuple형식으로 결합
        for item, value in enumerate(user_rank_list, start=1): 
            # request한 user의 id를 토대로 파싱하여, 순위를 rank의 추가       
            if value[f'author__user'] == user.id:
                rank.append(item)
    combined_data = list(zip(ranked_my_challenges, rank))

    # 참여자 TOP 5 릴렌지 (실시간)
    participants = Participant.objects.values('challenge_id').annotate(count=Count('user_id')).distinct()
    participants = participants.order_by('-count')
    participants_list = list(participants)
    best_challenges = []
    for i in range(0,len(participants_list)):
        best_challenge = participants_list[i]['challenge_id']
        rank_challenge = Challenge.objects.get(id=best_challenge)
        best_challenges.append(rank_challenge)
    challenge_ranking=[]
    for i in range(1, len(best_challenges) + 1):
        challenge_ranking.append((f'{i}', best_challenges[i-1]))
    if len(challenge_ranking) > 5:
        challenge_ranking = challenge_ranking[:5]

    # 유저의 나이대가 참여한 랭킹 순위
    # propert를 통해 생성된 것은 filter 적용 X -> birth를 기준으로 각자 나이대에 10대, 20대 등 나이대 설정
    age = datetime.now().year - user.birth
    min_age = 2023 - (age // 10 * 10)
    max_age = 2023 - ((age // 10 + 1) * 10)  
    # 나이대를 기준으로 설정한 birth를 통해 필터링
    participants = Participant.objects.filter(user__birth__lte=min_age, user__birth__gt=max_age)
    # valuse를 통해 group by 후에 distionct로 중복 제거, user_id를 통해 참여한 유저 수 세기
    participants = participants.values('challenge_id').annotate(count=Count('user_id')).distinct()
    # 참여한 유저수를 기준으로 정렬
    participants = participants.order_by('-count')
    participants_list = list(participants)
    age_challenge_rank=[]
    for i in range(0,len(participants_list)):
        age_challenge_id = participants_list[i]['challenge_id']
        age_challenge = Challenge.objects.get(id=age_challenge_id)
        age_challenge_rank.append(age_challenge)
    age_challenge_ranking=[]
    for i in range(1,len(age_challenge_rank) + 1):
        age_challenge_ranking.append((f'{i}', age_challenge_rank[i-1]))
    if len(age_challenge_ranking) > 5:
        age_challenge_ranking = age_challenge_ranking[:5]


    return render(request, 'main/ranking.html', {'combined_data': combined_data, 'challenge_ranking':challenge_ranking})
