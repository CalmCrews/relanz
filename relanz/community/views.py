from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import ArticleForm
from .models import Article

# Create your views here.

def communityHome(request):
    articles = Article.objects.all()
    
    paginator = Paginator(articles, 3) # 한페이지 당 사진 3개로 설정
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'community/communityHome.html', {'articles':articles, 'page_obj':page_obj})

def new(request):
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('community:detail', article.id)

    return render(request, 'community/new.html', {'form':form})

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    return render(request, 'community/detail.html', {'article':article})

def edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save()
            return redirect('community:detail', article.id)
    
    return render(request, 'community/edit.html', {'form':form, 'article':article})

def delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    article.delete()

    return redirect('main:home')