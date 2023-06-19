from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('<int:account_id>/', views.accountInfo, name="accountInfo"), #계정 마이페이지
    path('nickname/', views.nickname, name="nickname"), #닉네임 받아오기
    path('content/', views.content, name="content"), #나이랑 성별 받아오기
]
