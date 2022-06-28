from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board, name="board"),
    path('board/<int:id>/', views.detail, name="detail"),
    path('board/joinEnd', views.joinEnd, name="joinEnd"),
    path('menu/', views.menu, name="menu"),
    path('menu/<str:food>', views.stores, name="stores"),
    path('stores/<int:id>/', views.order, name="order"),
    path('stores/orderEnd', views.orderEnd, name="orderEnd"),
]