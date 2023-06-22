from django.urls import path
from . import views

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
]
