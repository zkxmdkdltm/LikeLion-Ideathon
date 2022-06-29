# Generated by Django 4.0.5 on 2022-06-30 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodCategory', models.CharField(choices=[('양식', '양식'), ('카페·디저트', '카페·디저트'), ('패스트푸드', '패스트푸드'), ('분식', '분식'), ('돈까스·회·일식', '돈까스·회·일식'), ('족발·보쌈', '족발·보쌈'), ('치킨', '치킨'), ('피자', '피자'), ('고기·구이', '고기·구이'), ('중식', '중식'), ('백반·죽·국수', '백반·죽·국수'), ('찜·찌개·탕', '찜·찌개·탕')], max_length=20)),
                ('name', models.CharField(max_length=10)),
                ('rate', models.FloatField()),
                ('tel', models.CharField(max_length=15)),
                ('min', models.IntegerField()),
                ('delivery_time', models.IntegerField()),
                ('delivery_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menus', models.JSONField(default=dict)),
                ('total', models.IntegerField(default=0)),
                ('host_option', models.CharField(choices=[('time', 'time'), ('button', 'button'), ('count', 'count')], max_length=10)),
                ('option_num', models.IntegerField(null=True)),
                ('pay_option', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[('주문중', '주문중'), ('결제전', '결제전'), ('주문완료', '주문완료')], default='결제전', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.store')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu', models.CharField(max_length=10)),
                ('price', models.IntegerField()),
                ('info', models.CharField(blank=True, max_length=30)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.store')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.CharField(max_length=256)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
