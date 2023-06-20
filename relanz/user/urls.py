from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('api/identify', views.identify, name="identify"),
    path('<int:user_id>/', views.userinfo, name="userinfo"), #계정 마이페이지
    path('nickname/', views.nickname, name="nickname"), #닉네임 받아오기
    path('content/', views.content, name="content"), #나이랑 성별 받아오기
]
