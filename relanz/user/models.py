from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

class User(AbstractUser):
    password = models.CharField(max_length=20, blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=32, unique=True, null=True)
    birth = models.IntegerField(null=True, default=0)
    
    sex_tuple = [
        ('male', 'male'),
        ('female', 'female')
    ]

    sex = models.CharField(max_length=10, choices=sex_tuple, null=True)

    @property
    def age(self):
        age_ = datetime.now().year - self.birth
        return age_

class Tag(models.Model):
    class Meta:
        db_table = 'tag'

    user = models.ForeignKey('User', on_delete=models.CASCADE, unique=True)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    evening = models.BooleanField(default=False)
    inside = models.BooleanField(default=False)
    outside = models.BooleanField(default=False)
    solo = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    extreme = models.BooleanField(default=False)
    calm = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    achievement = models.BooleanField(default=False)
    bodyhealth = models.BooleanField(default=False)
    confidence = models.BooleanField(default=False)
    mental = models.BooleanField(default=False)
    short = models.BooleanField(default=False)
    newtry = models.BooleanField(default=False)