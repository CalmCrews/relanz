from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from community.models import Article
from django.db.models import Sum, Count
from datetime import datetime
import random

def ranking(request):
    user=request.user
    if user.nickname is None or user.birth is None or user.sex is None:
        return redirect('user:content')
    
    # 실시간 TOP5 랭킹
    real_time_ranks = []
    # 현재 인증 글을 불러모아서 챌린지 아이디 기준으로 group by, 중복을 제거하고, 각각 인증글이 가지고 있는 score를 합해서 sum을 만들고, user_id를 통해 count를 만듦. 이 두 개를 기준을 정렬
    real_time_challenges=[]
    real_time_articles=Article.objects.values('challenge_id').distinct().annotate(sum=Sum('article_score'), count=Count('author_id__user_id')).order_by('-sum','-count')
    # 정렬한 순서를 기준으로 각각에 맞는 챌린지를 반환해서 리스트에 추가
    for real_time_article in real_time_articles:
        real_time_challenge = Challenge.objects.get(id=real_time_article['challenge_id'])
        real_time_challenges.append(real_time_challenge)
    # 반환한 챌린지에 순위를 매김
    for real_time_rank in enumerate(real_time_challenges,start=1):
        real_time_ranks.append(real_time_rank)
    
    if len(real_time_ranks) < 5:
        # 5개 이하일 시에는 참여자를 기준으로 추천 (실제 랭킹 X, 참여자수가 많은 만큼 추천하고 싶다의 의미)
        recommand_challenge_all=list(Challenge.objects.all())
        # 중복제거
        for x in real_time_challenges:
            if x in recommand_challenge_all:
                recommand_challenge_all.remove(x)
        # 추천챌린지 뽑기
        recommand_challenges=[]
        for recommand_challenge_rank in recommand_challenge_all:
            # 추천챌린지 뽑기 참여자를 기준으로 정렬해서 랭킹에 맞게 좀 더 의미있는 추천 알고리즘 구성
            recommand_challenge = Participant.objects.filter(challenge=recommand_challenge_rank)
            # 빈 쿼리 반환시 제거 후, 리스트에 추가 -> 추가할 때에는 쿼리셋이 아닌 딕셔너리 형태로 추가
            if recommand_challenge:
                recommand_challenge = recommand_challenge.values('challenge_id').distinct().annotate(count=Count('user_id'))
                recommand_challenges.append((recommand_challenge[0]))
        # count 값을 기준으로 정렬
        recommand_challenges = sorted(recommand_challenges, key=lambda x: x['count'], reverse=True)

        # 각각의 챌린지 아이디에 맞는 챌린지를 파싱
        recommand_challenges_ranks=[]
        for recommand_challenge in recommand_challenges:
            recommand_challenges_rank = Challenge.objects.get(id=recommand_challenge['challenge_id'])
            recommand_challenges_ranks.append(recommand_challenges_rank)

        # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
        recommand_number = [0] * len(recommand_challenges_ranks)
        recommand_challenges = list(zip(recommand_number, recommand_challenges_ranks))

        # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 5개까지만 파싱해서 전달
        for i in range(5 - len(real_time_challenges)):
            real_time_ranks.append(recommand_challenges[i])

        # 이렇게 해도 TOP 5를 채우지 못한다면 5개가 될 수 있도록 랜덤한 챌린지를 추천
        if len(real_time_ranks) < 5:
            remain_challenge_all=list(Challenge.objects.all())
            for x in real_time_challenges:
                # 중복 제거
                if x in remain_challenge_all:
                    remain_challenge_all.remove(x)
            for x in recommand_challenge_all:
                # 중복 제거
                if x in remain_challenge_all:
                    remain_challenge_all.remove(x)
            # 랜덤으로 부족한 랭킹 수 만큼 선택
            remain_challenge_random = random.sample(remain_challenge_all, k=5-len(real_time_ranks))
            # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
            remain_number = [0] * len(remain_challenge_random)
            remain_challenges = list(zip(remain_number, remain_challenge_random))
            # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 추천 챌린지를 찾은 만큼만 전달
            for i in range(5 - len(real_time_ranks)):
                real_time_ranks.append(remain_challenges[0])
            real_time_ranks_result=real_time_ranks[:5]
        else:
            real_time_ranks_result=real_time_ranks[:5]
    else:
        real_time_ranks_result=real_time_ranks[:5]
        

    # 유저의 나이대가 참여한 랭킹 순위
    age_ranks=[]
    # propert를 통해 생성된 것은 filter 적용 X -> birth를 기준으로 각자 나이대에 10대, 20대 등 나이대 설정
    age = datetime.now().year - user.birth
    min_age = 2023 - (age // 10 * 10)
    max_age = 2023 - ((age // 10 + 1) * 10)  


    # 나이대를 기준으로 설정한 birth를 통해 필터링
    age_articles_all = Article.objects.filter(author__user__birth__lte=min_age, author__user__birth__gt=max_age)

    # valuse를 통해 group by 후에 distinct로 중복 제거, user_id를 통해 참여한 유저 수 세기
    age_articles = age_articles_all.values('challenge_id').annotate(count=Count('author_id__user_id')).distinct().order_by('-count')
    
    age_challenges=[]
    for age_article in age_articles:
        age_challenge = Challenge.objects.get(id=age_article['challenge_id'])
        age_challenges.append(age_challenge)

    for age_challenge_rank in enumerate(age_challenges,start=1):
        age_ranks.append(age_challenge_rank)
    if len(age_ranks) < 5:
        # 5개 이하일 시에는 참여자를 기준으로 추천 (실제 랭킹 X, 참여자수가 많은 만큼 추천하고 싶다의 의미)
        recommand_challenges_all_age=[]
        recommand_ages = Participant.objects.values('challenge_id').distinct()
        for recommand_age in recommand_ages:
            recommand_challenge_all_age = Challenge.objects.get(id=recommand_age['challenge_id'])
            recommand_challenges_all_age.append(recommand_challenge_all_age)
        # 중복제거
        for x in age_challenges:
            if x in recommand_challenges_all_age:
                recommand_challenges_all_age.remove(x)

        # 추천챌린지 뽑기
        recommand_challenges_age=[]
        for recommand_challenge_rank_age in recommand_challenges_all_age:
            # 추천챌린지 뽑기 참여자를 기준으로 정렬해서 랭킹에 맞게 좀 더 의미있는 추천 알고리즘 구성
            recommand_challenge_age = Participant.objects.filter(challenge=recommand_challenge_rank_age)
            # 빈 쿼리 반환시 제거 후, 리스트에 추가 -> 추가할 때에는 쿼리셋이 아닌 딕셔너리 형태로 추가
            if recommand_challenge_age:
                recommand_challenge_age = recommand_challenge_age.values('challenge_id').distinct().annotate(count=Count('user_id'))
                recommand_challenges_age.append((recommand_challenge_age[0]))

        # count 값을 기준으로 정렬
        recommand_challenges_age = sorted(recommand_challenges_age, key=lambda x: x['count'], reverse=True)
        # 각각의 챌린지 아이디에 맞는 챌린지를 파싱
        recommand_challenges_ranks_age=[]
        for recommand_challenge_age in recommand_challenges_age:
            recommand_challenges_rank_age = Challenge.objects.get(id=recommand_challenge_age['challenge_id'])
            recommand_challenges_ranks_age.append(recommand_challenges_rank_age)

        # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
        recommand_number_age = [0] * len(recommand_challenges_ranks_age)
        recommand_challenges_age = list(zip(recommand_number_age, recommand_challenges_ranks_age))

        # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 5개까지만 파싱해서 전달
        for i in range(0, (5 - len(age_challenges))):
            age_ranks.append(recommand_challenges_age[i])

        # 이렇게 해도 TOP 5를 채우지 못한다면 5개가 될 수 있도록 랜덤한 챌린지를 추천
        if len(age_ranks) < 5:
            remain_challenge_all_age=list(Challenge.objects.all())
            for x in age_challenges:
                # 중복 제거
                if x in remain_challenge_all_age:
                    remain_challenge_all_age.remove(x)
            for x in recommand_challenges_all_age:
                # 중복 제거
                if x in remain_challenge_all_age:
                    remain_challenge_all_age.remove(x)
            # 랜덤으로 부족한 랭킹 수 만큼 선택
            remain_challenge_random_age = random.sample(remain_challenge_all_age, k=5-len(age_ranks))
            # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
            remain_number_age = [0] * len(remain_challenge_random_age)
            remain_challenges_age = list(zip(remain_number_age, remain_challenge_random_age))
            # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 추천 챌린지를 찾은 만큼만 전달
            for i in range(5 - len(age_ranks)):
                age_ranks.append(remain_challenges_age[0])
        else:
            age_ranks=age_ranks[:5]
    else:
        age_ranks=age_ranks[:5]

    female_ranking = gender_ranking('female')
    male_ranking = gender_ranking('male')
    if user.sex == 'male':
        res_ranking = {
            'male_ranking': male_ranking,
            'female_ranking': female_ranking,
        }
    res_ranking = {
        'male_ranking': male_ranking,
        'female_ranking': female_ranking,
    } 
    
    # 내가 쓴 글의 쿼리셋
    my_articles = Article.objects.filter(author__user=user).values('challenge_id')

    # 내가 참여하고 있는 챌린지 리스트
    if my_articles.exists():
        # 내가 쓴 글의 쿼리셋을 challenge를 기준으로 묶어서, score를 기준으로 정렬
        ranked_articles = my_articles.values('challenge').annotate(sum=Sum('article_score')).distinct().order_by('-sum')
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
            user_rank = article_list.values('author__user').annotate(sum=Sum('article_score')).distinct().order_by('-sum')

            # list에 순위를 기준으로 차례대로 list에 추가
            user_rank_list = list(user_rank)
            # list의 인덱스 번호를 토대로 순위를 tuple형식으로 결합
            for item, value in enumerate(user_rank_list, start=1): 
                # request한 user의 id를 토대로 파싱하여, 순위를 rank의 추가 
                if value[f'author__user'] == user.id:
                    rank.append((item, value))

        # participant -> 각 챌린지 마다 유저가 참여하고 있는 수
        all_challenge_ranking = []
        challenge_participants = []
        for my_challenge in ranked_my_challenges:
            challenge_participant = Article.objects.filter(challenge=my_challenge).values('challenge').annotate(count=Count('author__user_id'))
            challenge_participants.append(challenge_participant)
            for user_challenge_ranking in real_time_ranks:
                if my_challenge.id == user_challenge_ranking[1].id:
                    all_challenge_ranking.append(user_challenge_ranking[0])
        combined_data = list(zip(ranked_my_challenges, rank, all_challenge_ranking, challenge_participants))
        return render(request, 'main/ranking.html', {'combined_data':combined_data, 'challenge_ranking':real_time_ranks_result, 'res_ranking':res_ranking, 'age_challenge_ranking':age_ranks})
    else:
        return render(request, 'main/ranking.html', {'challenge_ranking':real_time_ranks, 'res_ranking':res_ranking, 'age_challenge_ranking':age_ranks})
    

def gender_ranking(sex):
    # 유저의 성별이 참여한 랭킹 순위
    gender_ranks=[]

    # 나이대를 기준으로 설정한 birth를 통해 필터링
    gender_articles_all = Article.objects.filter(author__user__sex=sex)

    # valuse를 통해 group by 후에 distinct로 중복 제거, user_id를 통해 참여한 유저 수 세기
    gender_articles = gender_articles_all.values('challenge_id').annotate(count=Count('author_id__user_id')).distinct().order_by('-count')
    
    gender_challenges=[]
    for gender_article in gender_articles:
        gender_article = Challenge.objects.get(id=gender_article['challenge_id'])
        gender_challenges.append(gender_article)

    for gender_challenge_rank in enumerate(gender_challenges,start=1):
        gender_ranks.append(gender_challenge_rank)
    if len(gender_ranks) < 5:
        # 5개 이하일 시에는 참여자를 기준으로 추천 (실제 랭킹 X, 참여자수가 많은 만큼 추천하고 싶다의 의미)
        recommand_challenges_all_gender=[]
        recommand_genders = Participant.objects.values('challenge_id').distinct()
        for recommand_gender in recommand_genders:
            recommand_challenge_all_gender = Challenge.objects.get(id=recommand_gender['challenge_id'])
            recommand_challenges_all_gender.append(recommand_challenge_all_gender)
        # 중복제거
        for x in gender_challenges:
            if x in recommand_challenges_all_gender:
                recommand_challenges_all_gender.remove(x)

        # 추천챌린지 뽑기
        recommand_challenges_gender=[]
        for recommand_challenge_rank_gender in recommand_challenges_all_gender:
            # 추천챌린지 뽑기 참여자를 기준으로 정렬해서 랭킹에 맞게 좀 더 의미있는 추천 알고리즘 구성
            recommand_challenge_gender = Participant.objects.filter(challenge=recommand_challenge_rank_gender)
            # 빈 쿼리 반환시 제거 후, 리스트에 추가 -> 추가할 때에는 쿼리셋이 아닌 딕셔너리 형태로 추가
            if recommand_challenge_gender:
                recommand_challenge_gender = recommand_challenge_gender.values('challenge_id').distinct().annotate(count=Count('user_id'))
                recommand_challenges_gender.append((recommand_challenge_gender[0]))

        # count 값을 기준으로 정렬
        recommand_challenges_gender = sorted(recommand_challenges_gender, key=lambda x: x['count'], reverse=True)
        # 각각의 챌린지 아이디에 맞는 챌린지를 파싱
        recommand_challenges_ranks_gender=[]
        for recommand_challenge_gender in recommand_challenges_gender:
            recommand_challenges_rank_gender = Challenge.objects.get(id=recommand_challenge_gender['challenge_id'])
            recommand_challenges_ranks_gender.append(recommand_challenges_rank_gender)

        # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
        recommand_number_gender = [0] * len(recommand_challenges_ranks_gender)
        recommand_challenges_gender = list(zip(recommand_number_gender, recommand_challenges_ranks_gender))

        # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 5개까지만 파싱해서 전달
        for i in range(0, (5 - len(gender_challenges))):
            gender_ranks.append(recommand_challenges_gender[i])
            
        # 이렇게 해도 TOP 5를 채우지 못한다면 5개가 될 수 있도록 랜덤한 챌린지를 추천
        if len(gender_ranks) < 5:
            remain_challenge_all_gender=list(Challenge.objects.all())
            for x in gender_challenges:
                # 중복 제거
                if x in remain_challenge_all_gender:
                    remain_challenge_all_gender.remove(x)
            for x in recommand_challenges_all_gender:
                # 중복 제거
                if x in remain_challenge_all_gender:
                    remain_challenge_all_gender.remove(x)
            # 랜덤으로 부족한 랭킹 수 만큼 선택
            remain_challenge_random_gender = random.sample(remain_challenge_all_gender, k=5-len(gender_ranks))
            # 파싱한 챌린지에 추천하는 챌린지라는 의미에서 0으로 고정
            remain_number_gender = [0] * len(remain_challenge_random_gender)
            remain_challenges_gender = list(zip(remain_number_gender, remain_challenge_random_gender))
            # 넘기는 리스트 데이터가 TOP 5가 될 수 있도록 추천 챌린지를 찾은 만큼만 전달
            for i in range(5 - len(gender_ranks)):
                gender_ranks.append(remain_challenges_gender[0])
        else:
            gender_ranks=gender_ranks[:5]
    else:
        gender_ranks=gender_ranks[:5]
    return gender_ranks