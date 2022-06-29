from email import message
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponseRedirect

from .models import User
from .forms import CustomUserChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.encoding import force_str, force_bytes
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        context = {}
        if User.objects.filter(username=request.POST['username']).exists():
            context['message'] = "아이디가 중복됩니다."
            return render(request, 'register.html', context)
        if User.objects.filter(nickname=request.POST['nickname']).exists():
            context['message'] = "닉네임이 중복됩니다."
            return render(request, 'register.html', context)
        if validate_password(request.POST['password']):
            context['message'] = "알맞지 않은 비밀번호 형식입니다."
            return render(request, 'register.html', context)
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST.get('username'),
                nickname=request.POST['nickname'],
                password=request.POST['password'],
                confirm=request.POST['confirm'],
                name=request.POST['name'],
                email=request.POST['email'],
                is_active = True,
            )
            user.save()
            current_site = get_current_site(request) 
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_b64encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            auth.login(request, user)
            return render(request, 'host.html')
    return render(request, 'register.html')
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'login.html', {'error' : '계정 활성화 오류'})
    
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'host.html')
        else:    
            context = {}
            context['message'] = "아이디와 비밀번호를 확인하세요"
            return redirect('/')
        
        
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def myinfo(request):
    return render(request, 'myInfo.html')


def myorders(request):
    return render(request, 'myorders.html')


@login_required
def myinfochange(request):
    if request.method == "POST":
        if User.objects.filter(nickname=request.POST['nickname']).exists():
            return render(request, 'myInfo.html', context={'context' : True})
        user = request.user
        user.nickname = request.POST['nickname']
        user.address = request.POST['address']
        user.save()
        return redirect('accounts:myinfo')
    return render(request, 'myInfo-change.html')

def validate_password(password):
    char = ['!', '@', '#', '$', '%', '^', '&', '*']
    flag = False
    for i in char:
        if i in password:
            flag = True
            break
    if (flag and (6 <= len(password) <= 16)):
        return True
    return False

