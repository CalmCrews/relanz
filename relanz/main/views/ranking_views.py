from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from community.models import Article
from django.db.models import Sum, Count
from datetime import datetime


# 성별에 따른 랭킹, 함수처리
def get_challenge_ranking(sex):
    # 성별에 따른 참여자 쿼리셋 생성
    participants = Participant.objects.filter(user__sex=sex)
    # 생성된 쿼리셋에서 challenge를 기준으로 group_by, 각 챌린지마다 유저 아이디 개수 생성, 생성된 개수를 바탕으로 정렬
    challenge_counts = participants.values('challenge_id').annotate(count=Count('user_id')).order_by('-count')[:5]
    # 챌린지 카운터를 기준으로 순위를 묶고, 딕셔너리 형태의 숫자 붙여서 tuple 생성
    challenge_ranking = [(f'{i+1}', Challenge.objects.get(id=item['challenge_id'])) for i, item in enumerate(challenge_counts)]
    return challenge_ranking

def ranking(request, user_id):
    user=request.user
    if user.nickname is None or user.birth is None or user.sex is None:
        return redirect('user:content')
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

    # 유저 성별별 TOP 5 릴렌지
    female_ranking = get_challenge_ranking('female')
    male_ranking = get_challenge_ranking('male')
    if user.sex == 'male':
        res_ranking = {
            'male_ranking': male_ranking,
            'female_ranking': female_ranking,
        }
    res_ranking = {
        'male_ranking': male_ranking,
        'female_ranking': female_ranking,
    } 
    # 내가 속한 챌린지의 랭킹
    participants = Participant.objects.filter(user=user)
    # 내가 참여하고 있는 챌린지 리스트
    if participants.exists():
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
        return render(request, 'main/ranking.html', {'combined_data':combined_data, 'challenge_ranking':challenge_ranking, 'res_ranking':res_ranking, 'age_challenge_ranking':age_challenge_ranking})
    else:
        return render(request, 'main/ranking.html', {'challenge_ranking':challenge_ranking, 'res_ranking':res_ranking, 'age_challenge_ranking':age_challenge_ranking})