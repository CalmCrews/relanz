from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

class User(AbstractUser):
    password = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=128, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=32, unique=True, null=True)
    birth = models.IntegerField(null=True, default=0)
    is_email_valid = models.BooleanField(default=False)
    
    sex_tuple = [
        ('male', 'male'),
        ('female', 'female')
    ]

    sex = models.CharField(max_length=10, choices=sex_tuple, null=True)
    
    avatar = models.CharField(max_length=30, null=True)

    @property
    def age(self):
        age_ = datetime.now().year - self.birth
        return age_
    
class UserTag(models.Model):
    class Meta:
        db_table = 'user_tag'

    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    #기본 태그
    morning = models.BooleanField(default=False, verbose_name='아침')  # 아침
    afternoon = models.BooleanField(default=False, verbose_name='점심')  # 점심
    evening = models.BooleanField(default=False, verbose_name='저녁')  # 저녁
    inside = models.BooleanField(default=False, verbose_name='실내')  # 실내
    outside = models.BooleanField(default=False, verbose_name='실외')  # 실외
    solo = models.BooleanField(default=False, verbose_name='혼자')  # 혼자
    group = models.BooleanField(default=False, verbose_name='여럿이')  # 여럿이
    pay = models.BooleanField(default=False, verbose_name='유료')  # 유료
    free = models.BooleanField(default=False, verbose_name='무료')  # 무료
    static = models.BooleanField(default=False, verbose_name='정적인')  # 정적인
    dynamic = models.BooleanField(default=False, verbose_name='동적인')  # 동적인
    #릴렌지 태그
    relaxation = models.IntegerField(default=0, verbose_name='피로해소')  # 피로해소
    immunity = models.IntegerField(default=0, verbose_name='면역력 향상')  # 면역력 향상
    easy = models.IntegerField(default=0, verbose_name='누구나 쉽게')  # 누구나 쉽게
    sleep = models.IntegerField(default=0, verbose_name='수면 개선')  # 수면 개선
    circulation = models.IntegerField(default=0, verbose_name='혈액순환 촉진')  # 혈액순환 촉진
    muscle = models.IntegerField(default=0, verbose_name='근육이완')  # 근육이완
    stability = models.IntegerField(default=0, verbose_name='정서 안정')  # 정서 안정
    concentration = models.IntegerField(default=0, verbose_name='집중력 향상')  # 집중력 향상
    creativity = models.IntegerField(default=0, verbose_name='창의력 발휘')  # 창의력 발휘
    satisfaction = models.IntegerField(default=0, verbose_name='만족감 증진')  # 만족감 증진
    achievement = models.IntegerField(default=0, verbose_name='성취감')  # 성취감
    depression = models.IntegerField(default=0, verbose_name='우울감 개선')  # 우울감 개선
    selfesteem = models.IntegerField(default=0, verbose_name='자아존중감 형성')  # 자아존중감 형성
    organization = models.IntegerField(default=0, verbose_name='감정 정리')  # 감정 정리
    expression = models.IntegerField(default=0, verbose_name='표현력 향상')  # 표현력 향상
    precision = models.IntegerField(default=0, verbose_name='꼼꼼함 향상')  # 꼼꼼함 향상
    easylearn = models.IntegerField(default=0, verbose_name='배우기 쉬운')  # 배우기 쉬운
    dexterity = models.IntegerField(default=0, verbose_name='손재주 향상')  # 손재주 향상
    motor = models.IntegerField(default=0, verbose_name='미세 운동 능력 발달')  # 미세 운동 능력 발달
    memory = models.IntegerField(default=0, verbose_name='기억력 향상')  # 기억력 향상
    skeletal = models.IntegerField(default=0, verbose_name='근육과 골격 강화')  # 근육과 골격 강화
    balance = models.IntegerField(default=0, verbose_name='균형감각 향상')  # 균형감각 향상
    flexibility = models.IntegerField(default=0, verbose_name='유연성 향상')  # 유연성 향상
    sociability = models.IntegerField(default=0, verbose_name='사회성 향상')  # 사회성 향상
    cooperation = models.IntegerField(default=0, verbose_name='협동성 향상')  # 협동성 향상
    bloodpressure = models.IntegerField(default=0, verbose_name='혈압 낮춤')  # 혈압 낮춤
    problemsolving = models.IntegerField(default=0, verbose_name='문제 해결 능력 향상')  # 문제 해결 능력 향상
    innerpeace = models.IntegerField(default=0, verbose_name='마음 진정')  # 마음 진정
    positive = models.IntegerField(default=0, verbose_name='긍정적인 생각')  # 긍정적인 생각
    mood = models.IntegerField(default=0, verbose_name='기분 전환')  # 기분 전환
    anxiety = models.IntegerField(default=0, verbose_name='불안 해소')  # 불안 해소
    bedtime = models.IntegerField(default=0, verbose_name='취침 전')  # 취침 전
    socialrelationship = models.IntegerField(default=0, verbose_name='사회적 관계 개선')  # 사회적 관계 개선
    newchallenge = models.IntegerField(default=0, verbose_name='새로운 도전')  # 새로운 도전
    friends = models.IntegerField(default=0, verbose_name='친구와 함께')  # 친구와 함께
    awareness = models.IntegerField(default=0, verbose_name='도전 의식')  # 도전 의식
    confidence = models.IntegerField(default=0, verbose_name='자신감') # 자신감
    output = models.IntegerField(default=0, verbose_name='산출물') # 산출물