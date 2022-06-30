from accounts.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Menu, Order, Store, Log
from django.http import HttpResponseRedirect
import requests


def board(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-create_at')
        paginator = Paginator(orders, 5)
        pagnum = request.GET.get('page')
        orders = paginator.get_page(pagnum)
        return render(request, 'board.html', {'orders': orders})


def detail(request, id):
    order = get_object_or_404(Order, pk=id)
    if order.author != request.user:
        menus = Menu.objects.all()
        menu = menus.filter(store=order.store)
        return render(request, 'detail.html', {'order': order, 'menu': menu})
    else:
        return HttpResponseRedirect('/accounts/myOrder/' + str(id))

def joinEnd(request):
    if request.method == 'POST':

        # menu append
        menu_total = 0
        user_menus = []
        for i in range(int(request.POST['total_count'])):
            user_menus.append({'food_id': request.POST['food'+str(i)], 'amount': request.POST['amount'+str(i)]})
            menu_total += get_object_or_404(Menu, pk=request.POST['food'+str(i)]).price
        
        order = get_object_or_404(Order, pk=request.POST['order_id'])
        order.menus[request.user.id] = user_menus
        order.total += menu_total
        order.save()


        # 카카오페이 결제 준비
        URL = 'https://kapi.kakao.com/v1/payment/ready'

        headers = {
            "Authorization": "KakaoAK " + "8113b3e4cef95643b26b5a0b702df4f2",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }

        params = { 
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": order.id,     # 주문번호
            "partner_user_id": request.user.id,    # 유저 아이디
            "item_name": "Weiter 금액 결제",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": menu_total + order.store.delivery_price,        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": "http://localhost:8000/order/pay/join",
            "cancel_url": "http://localhost:8000/order/joinFail/"+str(order.id),
            "fail_url": "http://localhost:8000/order/joinFail/"+str(order.id),
        }

        # 카카오페이 준비 api 요청 결과
        res = requests.post(URL, headers=headers, params=params)
        print(res.json())
        request.session['tid'] = res.json()['tid']
        request.session['order_id'] = order.id      # 결제 승인시 사용할 tid를 세션에 저장
        request.session.set_expiry(6000)
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url) 
        
def pay_join(request):
    order_id = request.session['order_id']
    tid = request.session['tid']
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
            "Authorization": "KakaoAK " + "8113b3e4cef95643b26b5a0b702df4f2",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
    
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": tid,  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": order_id,     # 주문번호
        "partner_user_id": request.user.id,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    log = Log(
        order = get_object_or_404(Order, pk=order_id),
        user = request.user,
        tid = tid
    )

    log.save()
    return render(request, 'joinEnd.html')


def joinFail(request):
    return render(request, 'joinFail.html')


def menu(request):
    return render(request, 'menu.html')


def stores(request, food):
    stores = Store.objects.all()
    stores = stores.filter(foodCategory=food)
    return render(request, 'stores.html', {'stores': stores})


def order(request, id):
    store = get_object_or_404(Store, pk=id)
    menus = Menu.objects.all()
    menu = menus.filter(store=store)
    return render(request, 'order.html', {'store': store, 'menu': menu})


def orderEnd(request):
    if request.method == 'POST':
        
        # order 정보 저장
        
        host_option = request.POST['host_option']
        option_num = None

        if host_option == "count":
            option_num = request.POST['option_count']
        elif host_option == "time":
            option_num = request.POST['option_time']

        # 총 메뉴 금액
        menu_total = 0

        # menu append
        user_menus = []
        for i in range(int(request.POST['total_count'])):
            user_menus.append({'food_id': request.POST['food'+str(i)], 'amount': request.POST['amount'+str(i)]})
            menu_total += get_object_or_404(Menu, pk=request.POST['food'+str(i)]).price

        menus = {}
        menus[request.user.id] = user_menus
        
        order = Order(
            state = "결제전",
            store = get_object_or_404(Store, pk=request.POST['store']),
            host_option = request.POST['host_option'],
            option_num = option_num,
            pay_option = int(request.POST['pay_option']),
            total = menu_total,
            menus = menus,
            author = get_object_or_404(User, id=request.user.id),
        )
        order.save()

        # 카카오페이 결제 준비
        URL = 'https://kapi.kakao.com/v1/payment/ready'

        headers = {
            "Authorization": "KakaoAK " + "8113b3e4cef95643b26b5a0b702df4f2",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }

        params = { 
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": order.id,     # 주문번호
            "partner_user_id": request.user.id,    # 유저 아이디
            "item_name": "Weiter 금액 결제",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": menu_total + order.store.delivery_price,        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": "http://localhost:8000/order/pay/approve",
            "cancel_url": "http://localhost:8000/order/orderFail/"+str(order.id),
            "fail_url": "http://localhost:8000/order/orderFail/"+str(order.id),
        }

        # 카카오페이 준비 api 요청 결과
        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']
        request.session['order_id'] = order.id      # 결제 승인시 사용할 tid를 세션에 저장
        request.session.set_expiry(6000)
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url) 

    elif request.method == 'GET':
        return render(request, 'orderEnd.html', {'order_id': order.id})


def pay_approve(request):
    order_id = request.session['order_id']
    tid = request.session['tid']
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
            "Authorization": "KakaoAK " + "8113b3e4cef95643b26b5a0b702df4f2",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
    
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": tid,  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": order_id,     # 주문번호
        "partner_user_id": request.user.id,    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)

    order = get_object_or_404(Order, pk=order_id)
    order.state = "주문중"
    order.save()

    log = Log(
        order = get_object_or_404(Order, pk=order_id),
        user = request.user,
        tid = tid
    )

    log.save()

    return render(request, 'orderEnd.html', {'order_id': order_id})


def orderFail(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    return HttpResponseRedirect('/')