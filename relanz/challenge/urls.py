from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'challenge'

urlpatterns = [
    path('<int:challenge_id>/', views.challenge, name="challenge"),
]