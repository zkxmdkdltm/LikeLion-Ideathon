from django.db import models


class Order(models.Model):
    STATE_CHOICES = {
        ('주문중', '주문중'),
        ('주문완료', '주문완료'),
    }

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

    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    menu = models.CharField(max_length=20, choices=MENU_CHOICES)
    location = models.CharField(max_length=10)
    store = models.CharField(max_length=10, null=True)
    author = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store


class Store(models.Model):
    MENU_CHOICES = {
        ('볶음밥', '볶음밥'),
        ('짬뽕', '짬뽕'),
    }

    name = models.CharField(max_length=10)
    rate = models.FloatField(null=True)
    min = models.IntegerField()
    delivery_time = models.IntegerField()
    delivery_price = models.IntegerField()
    menu = models.CharField(max_length=20, choices=MENU_CHOICES)

    def __str__(self):
        return self.name
