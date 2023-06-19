from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('user.urls')),
    path('account/', include('account.urls')),
    path('community/', include('community.urls')),
    path('challege/', include('challenge.urls')),
]


