from django.shortcuts import render, redirect
from .models import Challenge 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@login_required
def challenge(request, challenge_id):
    user=request.user
    if user.nickname is None:
            return redirect('user:content')
    challenge = Challenge.objects.get(id=challenge_id)
    return render(request, 'challenge/challenge.html', {'challenge':challenge})
