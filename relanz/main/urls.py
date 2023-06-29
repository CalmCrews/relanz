from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name="home"),
    path('ranking/<int:user_id>/', views.ranking, name="ranking"),
]
