from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from ..models import User
from django.core.mail import send_mail
import os
    
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

            return redirect('user:signin')
        
        except User.DoesNotExist:
            return render(request, 'user/findid.html', {'error': '일치하는 사용자가 없습니다.'})

    return render(request, 'user/findid.html')

