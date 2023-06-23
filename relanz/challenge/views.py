from django.shortcuts import render, redirect
from .models import Challenge 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

def challenge(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    return render(request, 'challenge/challenge.html', {'challenge':challenge})
