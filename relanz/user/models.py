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