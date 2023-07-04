from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


@login_required
def challenge(request, challenge_id):
	user=request.user
	if user.nickname is None:
			return redirect('user:content')
	challenge = Challenge.objects.get(id=challenge_id)
	challenge_tag = ChallengeTag.objects.get(challenge_id=challenge_id)
	
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
	participant_count = len(Participant.objects.filter(challenge=challenge_id))
	

	return render(request, 'challenge/challenge.html', {'challenge':challenge, 'challenge_tag':challenge_tag_list, 'participant':participant_count})



@login_required
def participate(request, challenge_id):
	user = request.user
	if user.nickname is None:
		return redirect('user:content')
	if Participant.objects.filter(user=user.id, challenge=challenge_id):
		return redirect("challenge:challenge", challenge_id)
	

	challenge = Challenge.objects.get(id=challenge_id)
	challenge_tag = ChallengeTag.objects.get(challenge=challenge_id)
	challenge_tag_dict = model_to_dict(challenge_tag)

	# 기본 태그 dictionary
	challenge_basic_tags = {
		'morning': challenge_tag.morning,
		'afternoon': challenge_tag.afternoon,
		'evening': challenge_tag.evening,
		'inside': challenge_tag.inside,
		'outside': challenge_tag.outside,
		'solo': challenge_tag.solo,
		'group': challenge_tag.group,
		'pay': challenge_tag.pay,
		'free': challenge_tag.free,
		'static': challenge_tag.static,
		'dynamic': challenge_tag.dynamic,
		}
	
	# 기본 태그 list
	challenge_basic_list=[]
	for tag_name, tag_value in challenge_basic_tags.items():
		if tag_value is True:
			challenge_basic_list.append(tag_name)
			

	# 챌린지가 갖고 있는 태그 list
	challenge_tag_list=[]
	challenge_tag_dict = model_to_dict(challenge_tag)
	for tag_name, tag_value in challenge_tag_dict.items():
		if tag_value is True and tag_name not in challenge_basic_list:
			challenge_tag_list.append(tag_name)  

	# user가 갖고 있는 tag 정보 갖고오기
	user_tag = UserTag.objects.get(user=user.id)

	# 챌린지가 갖고 있는 tag명을 이용해서 user_tag를 파싱후 +1 해주기
	for tag_name in challenge_tag_list:
		setattr(user_tag, tag_name, getattr(user_tag, tag_name) + 1)
	user_tag.save()

	participant = Participant(user=user, challenge=challenge)
	participant.save()

	res_data = {"user": user.nickname, 'challenge':challenge}
	return render(request, 'challenge/participate.html', res_data)

