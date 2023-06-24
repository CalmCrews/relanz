from django.contrib import admin
from .models import User, UserTag

# Register your models here.
admin.site.register(User)
admin.site.register(UserTag)