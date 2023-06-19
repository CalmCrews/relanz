from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'challenge'

urlpatterns = [
    path('<int:account_id>/', views.challenge, name="challenge"),
]