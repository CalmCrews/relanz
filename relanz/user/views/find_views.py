from django.shortcuts import render
from django.urls import reverse_lazy
from ..models import User
from django.core.mail import send_mail
import os
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.utils.translation import gettext as _

def findid(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            subject = f'회원님의 아이디는 {user.username}입니다.'
            message = f"회원님의 아이디는 {user.username}입니다. 이 메일은 회신불가입니다."
            from_email = os.environ.get('EMAIL_HOST_USER')
            recipient_list = [email]

            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            
            res_data = {'success': '입력하신 이메일로 아이디를 전송했습니다.'}

            return render(request, 'user/findid.html', res_data)
        
        # 일치하는 이메일 없으면 에러메시지 반환
        except User.DoesNotExist:

            res_data = {'error': '일치하는 사용자가 없습니다. 이메일을 다시 입력해주세요.'}
            
            return render(request, 'user/findid.html', res_data)

    return render(request, 'user/findid.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/custom_password_reset.html'
    email_template_name = 'user/custom_password_reset_email.html'
    subject_template_name = 'user/custom_password_reset_subject.txt'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/custom_password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user/custom_password_reset_confirm.html"

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/custom_password_reset_complete.html"