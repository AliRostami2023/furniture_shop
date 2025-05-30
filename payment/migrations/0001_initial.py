# Generated by Django 5.1.6 on 2025-04-03 17:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0005_remove_order_address_remove_order_city_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('first_name', models.CharField(max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(max_length=100, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(blank=True, max_length=150, null=True, verbose_name='ایمیل(اختیاری)')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('state', models.CharField(max_length=100, verbose_name='استان')),
                ('city', models.CharField(max_length=100, verbose_name='شهر')),
                ('zip_code', models.CharField(max_length=20, verbose_name='کد پستی')),
                ('address', models.CharField(max_length=300, verbose_name='آدرس')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_checkout', to='order.order', verbose_name='سفارش')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_checkout', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مشخصات گیرنده',
                'verbose_name_plural': 'مشخصات گیرندگان',
            },
        ),
    ]
