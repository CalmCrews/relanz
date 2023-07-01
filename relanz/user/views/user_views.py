from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from ..models import User
from django.contrib.auth import login, logout, authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages

# 이메일 인증 관련 import
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from user.tokens import account_activation_token


User = get_user_model()

@csrf_protect
def signup(request):
    if request.method=="GET":
        return render(request, 'user/signup.html')
    elif request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        res_data = {'username':username, 'password':password}
        if not (username and email and password and re_password):
            res_data['error']="입력되지 않은 값이 있습니다."
            return render(request, 'user/signup.html', res_data)
        elif (password != re_password):
            res_data['error']="비밀번호가 일치하지 않습니다."
            return render(request, 'user/signup.html', res_data)
        else:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()

            login(request, user)

            # email_sent(request)

            # return render(request, 'user/email_sent.html', {'user':user})
            return redirect('user:email_sent')
        
@csrf_exempt
def identify(request):
        json_data=json.loads(request.body)
        username = json_data.get('id')
        if User.objects.filter(username=username).exists():
            message = {'message': '이미 있는 아이디입니다.'}
            return JsonResponse(message, status=400)
        message = {'message': '사용가능한 아이디입니다.'}
        return JsonResponse(message, status=200)
        # return render(request, 'user/signup.html')

def signin(request):
    if request.method == "GET":
        return render(request,'user/signin.html')
    if request.method == "POST":
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            if not username:
                messages.add_message(request, messages.ERROR, '아이디')
                return render(request, 'user/signin.html')
            if not password:
                messages.add_message(request, messages.ERROR, '비밀번호')
                return render(request, 'user/signin.html')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) # 로그인은 되도록 설정
                if user.is_email_valid:
                    return redirect('main:home')
                else:
                    # email_sent(request)
                    # messages.add_message(request, messages.INFO, '이메일 인증을 완료해주세요. 이메일을 확인하세요.')
                    # return render(request, 'user/email_sent.html', {'user':user})
                    return redirect('user:email_sent')
            else:
                messages.add_message(request, messages.ERROR, '정보')
                return render(request, 'user/signin.html')
        else:
            return redirect('main:home')
                
def signout(request):
    logout(request)
    return redirect('main:home')


# 인증 메일 보내기
def email_sent(request):
    user = request.user
    
    if request.method == 'POST':
        if 'send_email' in request.POST:
            current_site = get_current_site(request)
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = user.email
            try:
                email = EmailMessage(mail_title, message, to=[mail_to])
                email.send()
                res_data = {'message': '메일 발송 완료.'}
                return JsonResponse(res_data)
            except Exception as e:
                res_data = {'error': '메일 발송 중 오류가 발생했습니다.'}
                return JsonResponse(res_data, status=500)
            
        elif 'complete_verification' in request.POST:
            if not user.is_email_valid:
                res_data = {'error': '인증이 완료되지 않았습니다. 다시 시도해주세요.'}
                return JsonResponse(res_data, status=500)
            else:
                return redirect('main:home')
    
        res_data = {'message': 'nothing happened'}
        return JsonResponse(res_data)
    return render(request, 'user/email_sent.html')


# 이메일 인증 후 유저 활성화
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_valid = True
        user.save()
        login(request, user)
        return redirect("main:home")
    else:
        res_data = {'error' : '계정 활성화 오류'}
        return redirect("user: email_sent", res_data, status=500)
    

# 하단바 더보기 페이지
def moreInfo(request, user_id):
    user=request.user
    return render(request, 'user/moreInfo.html', {"user":user})