# Generated by Django 3.2.13 on 2022-07-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_menu_info_alter_menu_menu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('결제전', '결제전'), ('주문완료', '주문완료'), ('주문중', '주문중')], default='결제전', max_length=10),
        ),
        migrations.AlterField(
            model_name='store',
            name='foodCategory',
            field=models.CharField(choices=[('치킨', '치킨'), ('패스트푸드', '패스트푸드'), ('백반·죽·국수', '백반·죽·국수'), ('찜·찌개·탕', '찜·찌개·탕'), ('고기·구이', '고기·구이'), ('중식', '중식'), ('족발·보쌈', '족발·보쌈'), ('피자', '피자'), ('양식', '양식'), ('카페·디저트', '카페·디저트'), ('돈까스·회·일식', '돈까스·회·일식'), ('분식', '분식')], max_length=20),
        ),
    ]
