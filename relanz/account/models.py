from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Account(models.Model):
    class Meta:
        db_table = "account"
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='account')
    nickname = models.CharField(max_length=32, unique=True, blank=False)
    birth = models.IntegerField(null=True, default=0)
    
    sex_tuple = [
        ('male', 'male'),
        ('female', 'female')
    ]

    sex = models.CharField(max_length=10, choices=sex_tuple, blank=False)   