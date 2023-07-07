from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article, Like, Participant
from user.models import User
from challenge.models import Challenge
from django.contrib.auth.decorators import login_required
from config.email_decorator import email_verified_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

import re, json

# Create your views here.
@csrf_exempt
@login_required(login_url='/user/signin')
@email_verified_required
def communityHome(request, challenge_id):
    user = request.user
    if request.method == 'GET':
        challenge = Challenge.objects.get(id=challenge_id)
         # a 챌린지의 게시물들만 가져오기
        articles = Article.objects.filter(challenge=challenge).order_by('-created_at')
         # 이 챌린지 참여했는지 안했는지 체크 위해 변수 만듬
        participated = Participant.objects.filter(user=user, challenge=challenge) 
        participants = len(Participant.objects.filter(challenge=challenge))
        # 한페이지 당 사진 9개로 설정
        paginator = Paginator(articles, 9) 
        try:
            page_number = request.GET.get('page')
            if page_number is not None and paginator.num_pages < int(page_number):
                message = {'message': '더 이상 기록이 없습니다.'}
                return JsonResponse(message, status=400)
            elif page_number is not None:
                page_obj = paginator.get_page(page_number)
                serialized_data = serializers.serialize('json', page_obj.object_list)
                return JsonResponse(serialized_data, safe=False, status=200)
            else:
                page_obj = paginator.get_page(page_number)

        except PageNotAnInteger:
            page = 1
            page_obj = paginator.get_page(page)

        except EmptyPage:
            page=paginator.num_pages
            page_obj=paginator.page(page)
            
        res_data = {'articles': articles, 'challenge':challenge, 'participated':participated, 'participants':participants,'articles':page_obj}

        return render(request, 'community/communityHome.html', res_data)
    if request.method == 'POST':
        user = request.user
        articles = Article.objects.filter(author__user = user, challenge=challenge_id)
        if articles.exists():
            current_time = timezone.now()
            articles = articles.order_by('-created_at')
            last_article = articles[0]
            time_difference = current_time - last_article.created_at
            if time_difference < timedelta(days=1):
                message = {'message': '릴렌지 기록은 하루에 한 번만 가능합니다.'}
                # return JsonResponse(message, status=400)
                messages.add_message(request, messages.ERROR, '릴렌지 기록은 하루에 한 번만 가능합니다')
                return redirect('community:communityHome', challenge_id)
            else:
                return redirect('community:new', challenge_id)
        else:
            return redirect('community:new', challenge_id)

@csrf_exempt
@login_required(login_url='/user/signin')
@email_verified_required
def new(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    try:
        participant = Participant.objects.get(user=request.user, challenge=challenge)
    
    # 챌린지에 참여하지 않았는데, 글을 작성하려고 할 때
    except Participant.DoesNotExist:
        return redirect('community:communityHome', challenge_id)
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = participant
            article.challenge = challenge
            article.user = request.user
            duplication_article = Article.objects.filter(author=participant, challenge=challenge)
            if duplication_article.exists():
                article.article_score = 100
            else:
                article.article_score = 500
            article.save()
            user=User.objects.get(id=request.user.id)
            user.score += article.article_score
            user.save()

        else:
            message = {'message': '사진 파일이 없습니다.'}
            return JsonResponse(message, status=400)
        messages.add_message(request, messages.SUCCESS, f'{article.article_score}')
        return redirect('community:detail', challenge.id, article.id)
    
    res_data = {'form':form, 'challenge':challenge}
    return render(request, 'community/new.html', res_data)

@login_required(login_url='/user/signin')
@email_verified_required
def detail(request, challenge_id, article_id):
    challenge = Challenge.objects.get(id=challenge_id)
    article = get_object_or_404(Article, pk=article_id)
    articles = Article.objects.filter(challenge=challenge).order_by('-created_at')
    participant = Participant.objects.filter(challenge_id=challenge_id)

    paginator = Paginator(articles, 1)
    try:     
        page_number = request.GET.get('page')
        print(page_number)
        if page_number is not None and paginator.num_pages < int(page_number):
                message = {'message': '더 이상 기록이 없습니다.'}
                return JsonResponse(message, status=400)
        else:
            page_obj = paginator.get_page(page_number)
            like_count = len(Like.objects.filter(article=page_obj.object_list[0]))
            author_nickname = page_obj.object_list[0].author.user.nickname
            isExist = Like.objects.filter(likedUser=request.user, article=page_obj.object_list[0]).exists() 
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.get_page(page)
        like_count = len(Like.objects.filter(article=article))
        author_nickname = article.author.user.nickname
        isExist = Like.objects.filter(likedUser=request.user, article=article).exists()
        
    except EmptyPage:
        page=paginator.num_pages
        page_obj=paginator.page(page)
        messages.add_message(request, messages.ERROR, '더 이상 인증 글이 없습니다.')
    
    res_data = {'challenge':challenge, 'articles':page_obj, 'like_count':like_count, 'author_nickname':author_nickname, "isExist": isExist, "participant":participant, "current":article}
    return render(request, 'community/detail.html', res_data)

@csrf_exempt
@login_required(login_url='/user/signin')
@email_verified_required
def edit(request, challenge_id, article_id):
    challenge = Challenge.objects.get(id=challenge_id)
    article = get_object_or_404(Article, pk=article_id)

    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save()
            return redirect('community:detail', challenge.id, article.id)
    
    res_data = {'form':form, 'challenge':challenge, 'article':article}
    return render(request, 'community/edit.html', res_data)

@login_required(login_url='/user/signin')
@email_verified_required
def delete(request, challenge_id, article_id):
    article = get_object_or_404(Article, pk=article_id)

    article.delete()

    return redirect('main:home')

@login_required(login_url='/user/signin')
@email_verified_required
def like(request, article_id):   
    article = get_object_or_404(Article, pk=article_id)

    referer = request.META.get('HTTP_REFERER')
    
    # 이미 좋아요 누른 경우 detail로 이동, 본인 글에 좋아요 누르기 가능
    isExist = Like.objects.filter(likedUser=request.user, article=article).exists()
    if isExist:
        try:
            get_object_or_404(Like, Q(article=article_id) & Q(likedUser=request.user.id)).delete()
        except:
            like_count = len(Like.objects.filter(article=article))
            likeCount = {
                    'likeCount': like_count,
                    "isClicked": isExist
            }
            messages.add_message(request, messages.ERROR, '다시 시도해주세요')
            return JsonResponse(likeCount, status=400)

        like_count = len(Like.objects.filter(article=article))
        likeCount = {
            'likeCount': like_count,
            "isClicked": isExist
        }
        # detail 페이지에서 좋아요를 시도할 때
        if referer:
            pattern = r'community/\d+/\d+'
            match = re.search(pattern, referer)
            if match:
                return JsonResponse(likeCount, status=200)
            
        return redirect("community:detail", challenge_id=article.challenge.id, article_id=article.id)

    # 좋아요 아직 안 누른 경우 Like 객체 만들기
    else:
        try:
            like = Like()
            like.article = get_object_or_404(Article, pk=article_id)
            like.likedUser = request.user
            like.save()
        except:
            messages.add_message(request, messages.ERROR, '다시 시도해주세요')
            like_count = len(Like.objects.filter(article=article))
            likeCount = {
                    'likeCount': like_count,
                    "isClicked": isExist
            }
            return JsonResponse(likeCount, status=400)

        like_count = len(Like.objects.filter(article=article))
        likeCount = {
                'likeCount': like_count,
                "isClicked": isExist
        }

        if referer:
            pattern = r'community/\d+/\d+'
            match = re.search(pattern, referer)
            if match:
                return JsonResponse(likeCount, status=200)
        return redirect('community:detail', challenge_id=article.challenge.id, article_id=article.id)


@login_required(login_url='/user/signin')
@email_verified_required
def myArticles(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    participant = Participant.objects.get(challenge=challenge, user=request.user)
    participant_count = Participant.objects.filter(challenge=challenge).count()

    if participant:
        articles = Article.objects.filter(challenge=challenge, author=participant)
        mediaList = [article.image.url for article in articles if article.image]
        zips = zip(mediaList, articles)

        res_data = {'challenge': challenge, 'participant':participant, 'participant_count':participant_count, 'articles': articles, 'mediaList': mediaList, 'zips':zips}
        return render(request, 'community/myArticles.html', res_data)
    
    return HttpResponse("No participants found for the current user and challenge.")