from django.urls import path
from .views import new, detail, edit, delete, communityHome

app_name = 'community'

urlpatterns = [
    path('communityHome/', communityHome, name='communityHome'),
    path('new/', new, name='new'),
    path('<int:article_id>', detail, name='detail'),
    path('edit/<int:article_id>', edit, name='edit'),
    path('delete/<int:article_id>', delete, name='delete'),
]