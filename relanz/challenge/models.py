from django.db import models

# Create your models here.
class challenge():
    class Meta:
        db_table="challenge"
    title_tuple = [
        ('climbing', '클라이밍'),
        ('walking', '산책하기')
    ]

    simple_tuple = [
        ()
    ]

    effect_tuple = [
        ()
    ]

    title = models.CharField(max_length=20, choices=title_tuple, blank=False)
    simple_effect = models.CharField(max_length=20, choices=title_tuple, blank=False)
    effect = models.CharField(max_length=20, choices=title_tuple, blank=False)
    recommnad = models.CharField(max_length=20, choices=title_tuple, blank=False)
    image = models.ImageField(upload_to='appname')
    