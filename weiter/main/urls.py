from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name="intro"),
    path('host/', views.host, name="host"),
    path('board/', views.board, name="board"),
    path('board/<int:id>/', views.detail, name="detail"),
    path('menu/', views.menu, name="menu"),
    path('stores/', views.stores, name="stores"),
    path('stores/<int:id>/', views.order, name="order"),
    path('stores/orderEnd', views.orderEnd, name="orderEnd"),
]
