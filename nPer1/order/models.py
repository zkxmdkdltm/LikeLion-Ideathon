from email.policy import default
from django.db import models

from accounts.models import User


class Store(models.Model):
    MENU_CHOICES = {
        ('피자', '피자'),
        ('패스트푸드', '패스트푸드'),
        ('양식', '양식'),
        ('카페·디저트', '카페·디저트'),
        ('돈까스·회·일식', '돈까스·회·일식'),
        ('분식', '분식'),
        ('백반·죽·국수', '백반·죽·국수'),
        ('찜·찌개·탕', '찜·찌개·탕'),
        ('고기·구이', '고기·구이'),
        ('중식', '중식'),
        ('족발·보쌈', '족발·보쌈'),
        ('치킨', '치킨'),
    }
    foodCategory = models.CharField(
        max_length=20, choices=MENU_CHOICES)
    name = models.CharField(max_length=10)
    rate = models.FloatField()
    tel = models.CharField(max_length=15)
    min = models.IntegerField()
    delivery_time = models.IntegerField()
    delivery_price = models.IntegerField()
    image = models.ImageField(upload_to = "store/")

    def __str__(self):
        return self.name


class Menu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu = models.CharField(max_length=10)
    price = models.IntegerField()
    info = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.menu

class Order(models.Model):
    Option_CHOICES = {
        ('button', 'button'),
        ('count', 'count'),
        ('time', 'time'),
    }

    STATE_CHOICES = {
        ('결제전', '결제전'),
        ('주문중', '주문중'),
        ('주문완료', '주문완료'),
    }

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menus = models.JSONField(default=dict)
    total = models.IntegerField(default=0)
    host_option = models.CharField(max_length=10, choices=Option_CHOICES)
    option_num = models.IntegerField(null=True)
    pay_option = models.BooleanField(default=True) # True: 각자 계산
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='결제전')

    def __str__(self):
            return self.store.name


class Log(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tid = models.CharField(max_length=256)
