from django.db import models

# Create your models here.
class Challenge(models.Model):
    class Meta:
        db_table="challenge"

    title = models.CharField(max_length=32, unique=True, blank=False)
    sub_effect = models.TextField(blank=False)
    effect = models.TextField(blank=False)
    recommand = models.TextField(blank=False)
    image = models.ImageField()

class Challenge_tag(models.Model):
    challengename = models.ForeignKey(Challenge, on_delete=models.CASCADE, unique=True)
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
    relaxation = models.BooleanField(default=False, verbose_name='피로해소')  # 피로해소
    immunity = models.BooleanField(default=False, verbose_name='면역력 향상')  # 면역력 향상
    easy = models.BooleanField(default=False, verbose_name='누구나 쉽게')  # 누구나 쉽게
    sleep = models.BooleanField(default=False, verbose_name='수면 개선')  # 수면 개선
    circulation = models.BooleanField(default=False, verbose_name='혈액순환 촉진')  # 혈액순환 촉진
    muscle = models.BooleanField(default=False, verbose_name='근육이완')  # 근육이완
    stability = models.BooleanField(default=False, verbose_name='정서 안정')  # 정서 안정
    concentration = models.BooleanField(default=False, verbose_name='집중력 향상')  # 집중력 향상
    creativity = models.BooleanField(default=False, verbose_name='창의력 발휘')  # 창의력 발휘
    satisfaction = models.BooleanField(default=False, verbose_name='만족감 증진')  # 만족감 증진
    achievement = models.BooleanField(default=False, verbose_name='성취감')  # 성취감
    depression = models.BooleanField(default=False, verbose_name='우울감 개선')  # 우울감 개선
    selfesteem = models.BooleanField(default=False, verbose_name='자아존중감 형성')  # 자아존중감 형성
    organization = models.BooleanField(default=False, verbose_name='감정 정리')  # 감정 정리
    expression = models.BooleanField(default=False, verbose_name='표현력 향상')  # 표현력 향상
    precision = models.BooleanField(default=False, verbose_name='꼼꼼함 향상')  # 꼼꼼함 향상
    easylearn = models.BooleanField(default=False, verbose_name='배우기 쉬운')  # 배우기 쉬운
    dexterity = models.BooleanField(default=False, verbose_name='손재주 향상')  # 손재주 향상
    motor = models.BooleanField(default=False, verbose_name='미세 운동 능력 발달')  # 미세 운동 능력 발달
    memory = models.BooleanField(default=False, verbose_name='기억력 향상')  # 기억력 향상
    skeletal = models.BooleanField(default=False, verbose_name='근육과 골격 강화')  # 근육과 골격 강화
    balance = models.BooleanField(default=False, verbose_name='균형감각 향상')  # 균형감각 향상
    flexibility = models.BooleanField(default=False, verbose_name='유연성 향상')  # 유연성 향상
    sociability = models.BooleanField(default=False, verbose_name='사회성 향상')  # 사회성 향상
    cooperation = models.BooleanField(default=False, verbose_name='협동성 향상')  # 협동성 향상
    bloodpressure = models.BooleanField(default=False, verbose_name='혈압 낮춤')  # 혈압 낮춤
    problemsolving = models.BooleanField(default=False, verbose_name='문제 해결 능력 향상')  # 문제 해결 능력 향상
    innerpeace = models.BooleanField(default=False, verbose_name='마음 진정')  # 마음 진정
    positive = models.BooleanField(default=False, verbose_name='긍정적인 생각')  # 긍정적인 생각
    mood = models.BooleanField(default=False, verbose_name='기분 전환')  # 기분 전환
    anxiety = models.BooleanField(default=False, verbose_name='불안 해소')  # 불안 해소
    bedtime = models.BooleanField(default=False, verbose_name='취침 전')  # 취침 전
    socialrelationship = models.BooleanField(default=False, verbose_name='사회적 관계 개선')  # 사회적 관계 개선
    newchallenge = models.BooleanField(default=False, verbose_name='새로운 도전')  # 새로운 도전
    friends = models.BooleanField(default=False, verbose_name='친구와 함께')  # 친구와 함께
    awareness = models.BooleanField(default=False, verbose_name='도전 의식')  # 도전 의식



