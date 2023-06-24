from django.shortcuts import render, redirect
from user.models import User, User_tag
from .models import Challenge, Challenge_tag, Participant
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


@login_required
def challenge(request, challenge_id):
	user=request.user
	if user.nickname is None:
			return redirect('user:content')
	challenge = Challenge.objects.get(id=challenge_id)
	challenge_tag = Challenge_tag.objects.get(challengename_id=challenge_id)
	
	# 챌린지가 갖고 있는 기본 태그
	challenge_basic_tags = {
		'아침': challenge_tag.morning,
		'점심': challenge_tag.afternoon,
		'저녁': challenge_tag.evening,
		'실내': challenge_tag.inside,
		'실외': challenge_tag.outside,
		'혼자': challenge_tag.solo,
		'여럿이': challenge_tag.group,
		'유료': challenge_tag.pay,
		'무료': challenge_tag.free,
		'정적인': challenge_tag.static,
		'동적인': challenge_tag.dynamic,
		}
	
	challenge_tag_list=[]
	for tag_name, tag_value in challenge_basic_tags.items():
		if tag_value is True:
			challenge_tag_list.append(tag_name)
	
	return render(request, 'challenge/challenge.html', {'challenge':challenge, 'challenge_tag':challenge_tag_list})



