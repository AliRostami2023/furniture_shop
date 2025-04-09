from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.html import format_html
from core.models import CreateMixin, UpdateMixin
from core.models import Image

User = get_user_model()


class CategoryProduct(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=300, verbose_name=_('عنوان'))
    slug = models.SlugField(max_length=80, allow_unicode=True, unique=True, verbose_name=_('عنوان در url'))
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('تصویر دسته بندی'))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and CategoryProduct.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=300, verbose_name=_('عنوان'))
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True, verbose_name=_('عنوان در url'))
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, related_name='category_product', verbose_name=_('دسته بندی'))
    price = models.PositiveIntegerField(_('قیمت محصول'))
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('تصویر محصول'))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_('درصد تخفیف'))
    rating = models.PositiveSmallIntegerField(_('امتیاز'), validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    width = models.CharField(max_length=20, verbose_name=_('عرض(سانتی متر)'))
    lenght = models.CharField(max_length=20, verbose_name=_('ارتفاع(سانتی متر)'))
    weight = models.CharField(max_length=20, verbose_name=_('وزن(سانتی متر)'))
    color = models.CharField(max_length=50, verbose_name=_('رنگ'))
    meterial = models.CharField(_('جنس محصول'), max_length=60)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Product.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def final_price(self):
        if not self.discount:
            return self.price
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        return self.price
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-create_at',)


class GalleryProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image', verbose_name=_('محصول'))
    image = models.ImageField(upload_to='images/gallery_product/%y/%m/%d', verbose_name=_('تصویر'))

    def __str__(self):
        return self.product.title
    
    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'گالری'



class CommentProduct(CreateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', verbose_name=_('کاربر'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment_product', verbose_name=_('محصول'))
    body = models.TextField(_('متن دیدگاه'))
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_('پاسخ'))

    def __str__(self):
        return self.user.full_name


    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'
        ordering = ('-create_at',)


class ProductFavorite(CreateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fproduct', verbose_name=_('محصول'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fuser', verbose_name=_('کاربر'))

    def __str__(self):
        return f"{self.product.title[:7]} - {self.user.full_name}"
    

    class Meta:
        verbose_name = _('محصول مورد علاقه')
        verbose_name_plural = _(' محصولات مورد علاقه کاربران')
