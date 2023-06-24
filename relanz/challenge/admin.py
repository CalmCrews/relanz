from django.contrib import admin
from .models import Challenge, ChallengeTag

# Register your models here.
admin.site.register(Challenge)
admin.site.register(ChallengeTag)