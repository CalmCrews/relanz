from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article

# Create your views here.

def new(request):
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('community:detail', id=article.id)

    return render(request, 'community/new.html', {'form':form})

def detail(request, id):
    article = get_object_or_404(Article, pk=id)

    return render(request, 'community/detail.html', {'article':article})

def edit(request, id):
    article = get_object_or_404(Article, pk=id)

    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            article = form.save()
            return redirect('community:detail', id=article.id)
    
    return render(request, 'community/edit.html', {'form':form, 'article':article})

def delete(request, id):
    article = get_object_or_404(Article, pk=id)

    article.delete()

    return redirect('main:home')