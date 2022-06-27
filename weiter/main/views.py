from django.shortcuts import render, get_object_or_404
from .models import Order, Store


def intro(request):
    return render(request, 'intro.html')


def host(request):
    return render(request, 'host.html')


def board(request):
    orders = Order.objects.all()
    return render(request, 'board.html', {'orders': orders})


def detail(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, 'detail.html', {'order': order})


def joinEnd(request):
    return render(request, 'joinEnd.html')


def menu(request):
    return render(request, 'menu.html')


def stores(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})


def order(request, id):
    store = get_object_or_404(Store, pk=id)
    return render(request, 'order.html', {'store': store})


def orderEnd(request):
    return render(request, 'orderEnd.html')
