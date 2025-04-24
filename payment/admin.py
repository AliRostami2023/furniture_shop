from django.contrib import admin
from .models import Checkout


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'first_name', 'last_name', 'address']
    search_fields = ['first_name', 'last_name', 'address']
    list_per_page = 20
