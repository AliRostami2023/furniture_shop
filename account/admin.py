from django.contrib import admin
from .models import *

admin.site.site_header = "مدیریت سایت"
admin.site.site_title = "فروشگاه مبلمان"
admin.site.index_title = "مدیریت سایت"


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'is_active', 'is_admin']
    list_filter = ['is_active', 'is_admin']
    search_fields = ['full_name', 'email', 'phone_number']
    list_per_page = 20
    inlines = [ProfileInline]


@admin.register(PasswordResetToken)
class PasswordReset(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_used']
    raw_id_fields = ['user']
    