from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('api/identify', views.identify, name="identify"),
    path('<int:user_id>/', views.userinfo, name="userinfo"), #계정 마이페이지
    path('content/', views.content, name="content"), #닉네임, 나이, 성별 받아오기 - 하나의 페이지로 통합
    # path('edit/<int:user_id>', views.accountedit, name='accountedit'), #프로필 수정
    path('survey/', views.survey, name="survey"), # 해소 정도 -> 닉네임, 나이, 성별 작성 후 가정 먼저 설문조사하는 페이지 (figma 참고)
    path('release/', views.release, name="release"), # 해소 방법 -> 해소 정도 조사 이후에 나타는 페이지
    path('activetime/', views.activetime, name="activetime"), # 활동 시간대 
    path('tagsurvey/', views.tagsurvey, name="tagsurvey"), # 유저의 tag 선택
    path('avatar/', views.avatar, name="avatar"), # 프로필 이미지
    path('findid/', views.findid, name="findid"), # 아이디 찾기

    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
]
