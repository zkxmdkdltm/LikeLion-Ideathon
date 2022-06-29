from django.urls import URLPattern, path
# from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import include

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('info_change/', views.myinfochange, name='info_change'),
    path('myorders/', views.myorders, name='myorders'),
    path('myOrder/<int:id>', views.myOrder, name='myOrder')
]
