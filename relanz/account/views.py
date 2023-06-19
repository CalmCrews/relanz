from django.shortcuts import render, redirect
from .models import Account


# Create your views here.
def nickname(request):
    account_data={}
    if request.method=="GET":
        return render(request, 'account/nickname.html')
    if request.method=="POST":
        nickname = request.POST.get('nickname')
        user = request.user
        
        if not nickname:
            account_data['error'] = "닉네임을 입력해주세요."
            return render(request, 'account/nickname.html', account_data)
        
        elif Account.objects.filter(nickname=nickname).exists():
            account_data['error'] = "이미 존재하는 닉네임입니다."
            return render(request, 'account/nickname.html', account_data)
        
        else:
            account = Account(nickname=nickname)
            account.user = user
            account.save()
            return redirect('account:content')



def content(request):
    if request.method=="GET":
        account = Account(user=request.user)
        return render(request, 'account/content.html', {'account':account})
    if request.method=="POST":
        account = Account.objects.get(user=request.user)
        birth = request.POST.get('birth')
        sex = request.POST.get('sex')
        account.birth = birth
        account.sex = sex
        account.save()
        return redirect('account:accountInfo', account.id)
    

def accountInfo(request, account_id):
    user = request.user
    account = Account.objects.get(user=user)
    account.birth = 2023 - account.birth
    return render(request, 'account/accountInfo.html', {'account': account})
