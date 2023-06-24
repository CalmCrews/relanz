from django.contrib import admin
from .models import User, User_tag

# Register your models here.
admin.site.register(User)
admin.site.register(User_tag)