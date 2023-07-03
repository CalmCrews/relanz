from django.urls import path
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('user_delete/', views.user_delete, name="user_delete"),
    path('api/identify', views.identify, name="identify"),
    path('userinfo/', views.userinfo, name="userinfo"), #계정 마이페이지
    path('content/', views.content, name="content"), #닉네임, 나이, 성별 받아오기 - 하나의 페이지로 통합
    path('moreInfo/', views.moreInfo, name="moreInfo"), # 하단바 더보기 페이지
    # path('<int:user_id>/moreInfo', views.moreInfo, name="moreInfo"), 
    
    path('survey/', views.survey, name="survey"), # 해소 정도 -> 닉네임, 나이, 성별 작성 후 가정 먼저 설문조사하는 페이지 (figma 참고)
    path('tagsurvey/', views.tagsurvey, name="tagsurvey"), # 유저의 tag 선택
    path('avatar/', views.avatar, name="avatar"), # 프로필 이미지
    path('findid/', views.findid, name="findid"), # 아이디 찾기

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('email_sent/', views.email_sent, name="email_sent"), # 이메일 전송
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"), # 이메일 인증 활성화
]
