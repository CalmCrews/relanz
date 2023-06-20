from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=32, unique=True, blank=False)
    birth = models.IntegerField(null=True, default=0)
    
    sex_tuple = [
        ('male', 'male'),
        ('female', 'female')
    ]

    sex = models.CharField(max_length=10, choices=sex_tuple, blank=False)

