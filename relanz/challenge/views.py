from django.shortcuts import render, redirect
from user.models import User, User_tag
from .models import Challenge, Challenge_tag, Participant
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict





