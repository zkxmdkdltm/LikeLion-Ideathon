# Generated by Django 4.0.5 on 2022-06-27 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_store_alter_order_menu_alter_order_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='menu',
            field=models.CharField(choices=[('양식', '양식'), ('돈까스·회·일식', '돈까스·회·일식'), ('중식', '중식'), ('고기·구이', '고기·구이'), ('족발·보쌈', '족발·보쌈'), ('백반·죽·국수', '백반·죽·국수'), ('카페·디저트', '카페·디저트'), ('찜·찌개·탕', '찜·찌개·탕'), ('치킨', '치킨'), ('패스트푸드', '패스트푸드'), ('피자', '피자'), ('분식', '분식')], max_length=20),
        ),
        migrations.AlterField(
            model_name='store',
            name='delivery_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='store',
            name='menu',
            field=models.CharField(choices=[('볶음밥', '볶음밥'), ('짬뽕', '짬뽕')], max_length=20),
        ),
        migrations.AlterField(
            model_name='store',
            name='rate',
            field=models.FloatField(null=True),
        ),
    ]
