from email import message
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponseRedirect

from .models import User
from order.models import Order, Store, Menu, Log
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
                address=request.POST['address'],
                address_detail=request.POST['address_detail'],
                email=request.POST['email'],
                is_active = True,
            )
            user.save()
            # current_site = get_current_site(request) 
            # message = render_to_string('activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_b64encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # mail_title = "계정 활성화 확인 이메일"
            # mail_to = request.POST["email"]
            # email = EmailMessage(mail_title, message, to=[mail_to])
            # email.send()
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
    print(request.user.address_detail)
    return render(request, 'myInfo.html')

"""
host option 주문 종료 방법 
option num 몇 명 혹은 몇 분에 대한 정보
pay option bool 트루가 각자 계산 / 펄스 호스트가 한 번에 계산
total 총 주문 금액
"""



def myOrder(request, id):
    order = get_object_or_404(Order,pk=id)
    user = User.objects.get(username=order.author)
    
    pay_option = "호스트가 한 번에 계산"
    if (order.pay_option):
        pay_option = "각자 계산"
        
    host_option = "호스트가 종료"
    if (order.host_option == "time"):
        host_option = "시간이 만료"
    elif (order.host_option == ""):
        host_option = "정원 충족"
            
    menus = order.menus
    my_menu = []
    other_menu = []
    menu = {}
    total = order.store.delivery_price

    for key in list(menus.keys()):
        temp_list = []
        temp_dic = {}        
        for i in range(len(menus[key])):
            temp_dic = {}               
            store = menus[key][i]
            food = get_object_or_404(Menu, pk=int(store["food_id"])) 
            temp_dic["name"] = food.menu
            temp_dic["amount"] = store["amount"]
            temp_dic["price"] = int(store["amount"]) * int(food.price)
            total += temp_dic["price"]
            temp_list.append(temp_dic)
            
            if food.menu in list(menu.keys()):
                menu[food.menu] += temp_dic["price"]
            else:
                menu[food.menu] = temp_dic["price"]
                
        if int(request.user.id) == int(key):
            my_menu = temp_list
        else:
            other_menu += temp_list
            
    menus = []
    for key in list(menu.keys()):
        temp = dict()
        temp["name"] = key
        temp["price"] = menu[key]
        menus.append(temp)
    
    context = {
        'host_id' : user.id,
        'order' : order,
        'store' : order.store,
        'host_option' : host_option,
        'total' : total,
        'pay_option' : pay_option,
        'my_menu': my_menu,
        'other_menu' : other_menu,
        'menus' : menus,
    }
    
    return render(request, 'myOrder.html', context)

def myorders(request , id):
    orders = Order.objects.all()
    user = get_object_or_404(User, pk=id)
    value = []
    # 오더 안에 메뉴 안에 번호들이 유저 번호
    
    for order in orders:
        # 내가 글쓴 사람일 경우 추가
        if int(user.id) in list(map(int, order.menus)):
            value.append(order)
            continue
        # 내가 글에 참여한 사람일 경우 추가
        for order_id in order.menus:
            if int(order_id) == int(user.id):
                value.append(order)
                break
    value = sorted(value, key=lambda x : x.create_at, reverse=True)
    context = {
        'orders' : value
    }
    
    return render(request, 'myorders.html', context)

def orderCancel(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    return render(request, 'host.html')

def payEnd(request, id):
    order = get_object_or_404(Order,pk=id)
    logs = Log.objects.filter(order=order)
    delivery_price = order.store.delivery_price
    person = len(order.menus)
        
    # 거스름돈 반환용 카카오페이 결제취소
    URL = 'https://kapi.kakao.com/v1/payment/cancel'

    headers = {
            "Authorization": "KakaoAK " + "8113b3e4cef95643b26b5a0b702df4f2",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
    }

    for log in logs:

        cancel_amount = delivery_price - math.floor(delivery_price/person)
        params = { 
                "cid": "TC0ONETIME",    # 테스트용 코드
                "tid": log.tid,
                "cancel_amount": cancel_amount,
                "cancel_tax_free_amount": "0",
        }
        res = requests.post(URL, headers=headers, params=params)

    order.state = "주문완료"
    order.save()

    return render(request, 'payEnd.html', context={'order' : order})

@login_required
def myinfochange(request):
    if request.method == "POST":
        if User.objects.filter(nickname=request.POST['nickname']).exists():
            return render(request, 'myInfo.html', context={'context' : True})
        user = request.user
        user.nickname = request.POST['nickname']
        user.address = request.POST['address']
        user.address_detail = request.POST['address_detail']
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
        return False
    return True

