from django.shortcuts import render, redirect
from user.models import User, UserTag
from challenge.models import Challenge, ChallengeTag, Participant
from django.forms.models import model_to_dict
from django.db.models import Q


# Create your views here.
def home(request):
    user=request.user
    if request.user.is_authenticated:
        try:
            user_tag = UserTag.objects.get(user=user.id)
            participant = Participant.objects.get(user=user.id)
            basic_tags_ = {
            '아침': user_tag.morning,
            '점심': user_tag.afternoon,
            '저녁': user_tag.evening,
            '실내': user_tag.inside,
            '야외': user_tag.outside,
            '혼자': user_tag.solo,
            '여럿이': user_tag.group,
            '정적인': user_tag.static,
            '동적인': user_tag.dynamic,
            }
            tag_lists_=[]
            for tag_name, tag_value in basic_tags_.items():
                if tag_value is True:
                    tag_lists_.append(tag_name)

            basic_tags = {
            'morning': user_tag.morning,
            'afternoon': user_tag.afternoon,
            'evening': user_tag.evening,
            'inside': user_tag.inside,
            'outside': user_tag.outside,
            'solo': user_tag.solo,
            'group': user_tag.group,
            'pay': user_tag.pay,
            'free': user_tag.free,
            'static': user_tag.static,
            'dynamic': user_tag.dynamic,
            }

            tag_lists=[]
            for tag_name, tag_value in basic_tags.items():
                if tag_value is True:
                    tag_lists.append(tag_name)
            challenges = ChallengeTag.objects.filter(**{tag_list: True for tag_list in tag_lists})

            minus_tag = ['id','user']
            for tag_name, tag_value in basic_tags.items():
                minus_tag.append(tag_name)
            
            user_tag_dict = model_to_dict(user_tag)
            for i in range(0, len(minus_tag)):
                del user_tag_dict[f'{minus_tag[i]}']
            sorted_user_tag = sorted(user_tag_dict.items(), key=lambda x:x[1], reverse=True)
            sorted_user_keys = [item[0] for item in sorted_user_tag]

            
            c1_query =Q()
            for key in sorted_user_keys[:3]:
                c1_query |=Q(**{key: True})
            c2_query=Q()
            for key in tag_lists:
                c2_query |=Q(**{key: True})
            challenge_query = c1_query|c2_query
            
            challenge_tags = ChallengeTag.objects.filter(challenge_query).order_by(f'-{sorted_user_keys[0]}', f'-{sorted_user_keys[1]}', f'-{sorted_user_keys[2]}')
            challenge_ids  = challenge_tags.values_list('challengename', flat=True)
            challenges = Challenge.objects.filter(id__in=challenge_ids)
            challenge_order = {challenge_id: order for order, challenge_id in enumerate(challenge_ids)}
            sorted_challenges = sorted(challenges, key=lambda c: challenge_order.get(c.id, float('inf')))

            return render(request, 'main/home.html', {'user':user, 'tag_lists':tag_lists_, 'challenges':sorted_challenges})
        except UserTag.DoesNotExist:
            user_tag = UserTag.objects.create(user=user)
            return render(request, 'main/home.html', {'user':user})
        except Participant.DoesNotExist:
            basic_tags_ = {
            '아침': user_tag.morning,
            '점심': user_tag.afternoon,
            '저녁': user_tag.evening,
            '실내': user_tag.inside,
            '야외': user_tag.outside,
            '혼자': user_tag.solo,
            '여럿이': user_tag.group,
            '정적인': user_tag.static,
            '동적인': user_tag.dynamic,
            }
            tag_lists_=[]
            for tag_name, tag_value in basic_tags_.items():
                if tag_value is True:
                    tag_lists_.append(tag_name)
            print(tag_lists_)
            basic_tags = {
            'morning': user_tag.morning,
            'afternoon': user_tag.afternoon,
            'evening': user_tag.evening,
            'inside': user_tag.inside,
            'outside': user_tag.outside,
            'solo': user_tag.solo,
            'group': user_tag.group,
            'pay': user_tag.pay,
            'free': user_tag.free,
            'static': user_tag.static,
            'dynamic': user_tag.dynamic,
            }

            tag_lists=[]
            for tag_name, tag_value in basic_tags.items():
                if tag_value is True:
                    tag_lists.append(tag_name)
            challenge_query = Q()
            for tag_list in tag_lists:
                challenge_query |= Q(**{tag_list: True})
            challenges = ChallengeTag.objects.filter(challenge_query)
            return render(request, 'main/home.html', {'user':user, 'tag_lists':tag_lists_, 'challengs':challenges})
        
            
    return render(request, 'main/splashscreen.html')
