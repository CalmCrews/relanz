from django.db import models
from user.models import User

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='')

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    likedUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)