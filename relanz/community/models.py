from django.db import models
from user.models import User
from challenge.models import Participant, Challenge

# Create your models here.

class Article(models.Model):
    challenge = models.ForeignKey(Challenge, default=1, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='')
    article_score = models.IntegerField(default=0)

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    likedUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)