from django.shortcuts import render
from django.urls import reverse_lazy
from ..models import User
from django.core.mail import send_mail
import os
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
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
            
            res_data = {'success': '입력하신 이메일로 아이디가 전송되었습니다'}

            return render(request, 'user/findid.html', res_data)
        
        # 일치하는 이메일 없으면 에러메시지 반환
        except User.DoesNotExist:

            res_data = {'error': '일치하는 사용자가 없습니다. 이메일을 다시 입력해주세요.'}
            
            return render(request, 'user/findid.html', res_data)

    return render(request, 'user/findid.html')


# 비밀번호 재설정 커스터마이징을 위한 상속
class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/pw_reset.html'
    email_template_name = 'user/pw_reset_email.html'
    subject_template_name = 'user/pw_reset_subject.txt'
    success_url = reverse_lazy("user:password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/pw_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user/pw_reset_confirm.html"
    success_url = reverse_lazy("user:password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/pw_reset_complete.html"