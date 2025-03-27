from django.contrib import admin
from .models import *


class FooterBoxInline(admin.TabularInline):
    model = FooterLink


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'subject', 'content', 'create_at']
    search_fields = ['full_name', 'email', 'phone_number']
    list_per_page = 20


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'content', 'create_at']


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'full_name', 'position']


@admin.register(SliderHome)
class SliderHomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'url']


@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'url']


@admin.register(FooterBox)
class FooterBoxAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']
    inlines = [FooterBoxInline]


@admin.register(InformationShop)
class InformationShopAdmin(admin.ModelAdmin):
    list_display = ['telegram', 'instagram', 'whatsapp', 'phone_number', 'email', 'address']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['icon_tag', 'title', 'desc']
