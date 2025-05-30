# Generated by Django 5.1.6 on 2025-02-18 19:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپدیت')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=80, unique=True, verbose_name='عنوان در url')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('update_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپدیت')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=80, unique=True, verbose_name='عنوان در url')),
                ('content', models.TextField(verbose_name='متن مقاله')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_blog', to='core.image', verbose_name='تصویر مقاله')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_blog', to='blog.categoryblog', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='CommentBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('body', models.TextField(verbose_name='متن دیدگاه')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_blog', to='blog.blog', verbose_name='lrhgi')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repliess', to='blog.commentblog', verbose_name='پاسخ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user_blog', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دیدگاه',
                'verbose_name_plural': 'دیدگاه ها',
                'ordering': ('-create_at',),
            },
        ),
    ]
