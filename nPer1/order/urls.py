from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('board/', views.board, name="board"),
    path('board/<int:id>/', views.detail, name="detail"),
    path('board/joinEnd', views.joinEnd, name="joinEnd"),
    path('joinFail/', views.joinFail, name="joinFail"),
    path('menu/', views.menu, name="menu"),
    path('menu/<str:food>', views.stores, name="stores"),
    path('stores/<int:id>/', views.order, name="order"),
    path('stores/orderEnd', views.orderEnd, name="orderEnd"),
    path('orderFail/<int:id>', views.orderFail, name="orderFail"),
    path('pay/approve', views.pay_approve, name="pay_approve"),
    path('pay/join', views.pay_join, name="payJoin"),
]