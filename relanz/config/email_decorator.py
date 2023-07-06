from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# 이메일 인증 접근 차단 관리
def email_verified_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        # 이메일 인증 한 경우
        if hasattr(user, 'is_email_valid') and user.is_email_valid:
            return view_func(request, *args, **kwargs)
        
        # 이메일 인증 안한 경우 -> 접근 차단 메세지
        else:
            message = {'message': '이메일 인증을 완료해주세요'}
            # return JsonResponse(message)
            return redirect('user:email_sent')
    return wrapper