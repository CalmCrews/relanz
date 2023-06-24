from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant

# Create your views here.
def home(request):
    user=request.user
    if request.user.is_authenticated:
        user_tag = UserTag.objects.get(user=user.id)
        basic_tags = {
        'morning': user_tag.morning,
        'afternoon': user_tag.afternoon,
        'evening': user_tag.evening,
        'inside': user_tag.inside,
        'outside': user_tag.outside,
        'solo': user_tag.solo,
        'group': user_tag.group,
        'extreme': user_tag.pay,
        'calm': user_tag.free,
        'focus': user_tag.static,
        'achievement': user_tag.dynamic,
        }
        user_tag_list=[]
        for tag_name, tag_value in basic_tags.items():
            if tag_value is True:
                user_tag_list.append(tag_name)

        return render(request, 'main/home.html', {'user':user})
    return render(request, 'main/splashscreen.html')
