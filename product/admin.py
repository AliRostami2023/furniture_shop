from django.contrib import admin
from .models import *
from core.models import Image


admin.site.register(Image)


class GalleryProductInline(admin.TabularInline):
    model = GalleryProduct


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'category', 'price', 'width', 'lenght', 'weight', 'color', 'meterial']
    list_per_page = 20
    inlines = [GalleryProductInline]


@admin.register(CommentProduct)
class CommentProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'body', 'reply', 'create_at']
    search_fields = ['user', 'product', 'body']


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    search_fields = ['user', 'product']

