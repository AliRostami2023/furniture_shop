from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from core.models import CreateMixin, UpdateMixin
from core.models import Image

User = get_user_model()


class CategoryBlog(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=300, verbose_name=_('عنوان'))
    slug = models.SlugField(max_length=80, allow_unicode=True, unique=True, verbose_name=_('عنوان در url'))

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Blog(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=300, verbose_name=_('عنوان'))
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True, verbose_name=_('عنوان در url'))
    category = models.ForeignKey(CategoryBlog, on_delete=models.CASCADE, related_name='category_blog', verbose_name=_('دسته بندی'))
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image_blog', verbose_name=_('تصویر مقاله'))
    content = models.TextField(_('متن مقاله'))

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))
    
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-create_at',)


class CommentBlog(CreateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user_blog', verbose_name=_('کاربر'))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment_blog', verbose_name=_('lrhgi'))
    body = models.TextField(_('متن دیدگاه'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='repliess', verbose_name=_('پاسخ'))

    def __str__(self):
        return self.user.full_name


    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        ordering = ('-create_at',)