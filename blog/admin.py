from django.contrib import admin
from .models import *


@admin.register(CategoryBlog)
class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'content']
    list_per_page = 20
    search_fields = ['title', 'category', 'content']


@admin.register(CommentBlog)
class CommentBlog(admin.ModelAdmin):
    list_display = ['user', 'blog', 'body', 'reply', 'create_at']
    raw_id_fields = ['user', 'blog']
    search_fields = ['user', 'blog', 'body']
