from accounts.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .models import Menu, Order, Store
from django.http import HttpResponseRedirect


def board(request):
    if request.method == 'GET':
        orders = Order.objects.all()
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
        return HttpResponseRedirect('/accounts/myorder/' + str(id))

def joinEnd(request):
    if request.method == 'POST':

        # menu append
        user_menus = []
        for i in range(int(request.POST['total_count'])):
            user_menus.append({'food_id': request.POST['food'+str(i)], 'amount': request.POST['amount'+str(i)]})
        
        order = get_object_or_404(Order, pk=request.POST['order_id'])
        order.menus[request.user.id] = user_menus
        order.save()
        
        return render(request, 'joinEnd.html')


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
        
        host_option = request.POST['host_option']
        option_num = None

        if host_option == "count":
            option_num = request.POST['option_count']
        elif host_option == "time":
            option_num = request.POST['option_time']

        # menu append
        user_menus = []
        for i in range(int(request.POST['total_count'])):
            user_menus.append({'food_id': request.POST['food'+str(i)], 'amount': request.POST['amount'+str(i)]})

        menus = {}
        menus[request.user.id] = user_menus

        order = Order(
            store = get_object_or_404(Store, pk=request.POST['store']),
            host_option = request.POST['host_option'],
            option_num = option_num,
            pay_option = int(request.POST['pay_option']),
            total = 0,
            menus = menus,
            author = get_object_or_404(User, id=request.user.id),
        )
        order.save()
        order_id = order.id
        return render(request, 'orderEnd.html', {'order_id': order_id})


def orderFail(request, id):
    order = get_object_or_404(Order, pk=id)
    order.delete()
    redirect('intro')
