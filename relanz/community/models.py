from django.db import models
from user.models import User
from challenge.models import Participant, Challenge

# Create your models here.

class Article(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE, related_name='articles') # Participant가 작성한 글 유저와 연결 위해 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='')

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    likedUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)