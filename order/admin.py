from django.contrib import admin
from .models import *


class DetailInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'is_paid']
    list_filter = ['is_paid', 'status']
    raw_id_fields = ['user']
    search_fields = ['user']
    list_per_page = 20
    inlines = [DetailInline]


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_per_page = 20
    
