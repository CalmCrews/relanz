from django.urls import path
from .views import new, detail, edit, delete
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('new/', new, name='new'),
    path('<int:article_id>', detail, name='detail'),
    path('edit/<int:article_id>', edit, name='edit'),
    path('delete/<int:article_id>', delete, name='delete'),
]