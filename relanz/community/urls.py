from django.urls import path
from .views import new, detail, edit, delete, communityHome, like

app_name = 'community'

urlpatterns = [
    path('communityHome/<int:challenge_id>', communityHome, name='communityHome'),
    path('<int:challenge_id>/<int:article_id>', detail, name='detail'),
    path('<int:challenge_id>/new', new, name='new'),
    path('edit/<int:challenge_id>/<int:article_id>', edit, name='edit'),
    path('delete/<int:challenge_id>/<int:article_id>', delete, name='delete'),
    path('<int:article_id>/like/', like, name='like')
]