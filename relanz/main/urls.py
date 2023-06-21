from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name="home"),
    # 이인이 signin.html 연결해볼라고 임시로 만듬
    # path('login/', views.login, name="login"), 
    # 주석 처리 할게요
]