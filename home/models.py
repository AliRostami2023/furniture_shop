from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from core.models import CreateMixin



class ContactUs(CreateMixin):
    full_name = models.CharField(max_length=300, verbose_name=_('نام و نام خانوادگی'))
    email = models.EmailField(max_length=300, verbose_name=_('ایمیل'))
    phone_number = models.CharField(max_length=11, verbose_name=_('شماره همراه'))
    subject = models.CharField(max_length=300, verbose_name=_('موضوع پیام'))
    content = models.TextField(max_length=2048, verbose_name=_('متن پیام'))

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = _('ارتباط با ما')
        verbose_name_plural = _('پیام های مشتریان')


class AboutUs(CreateMixin):
    image = models.ImageField(upload_to='images/about_us', verbose_name=_('عکس'))
    content = models.TextField(_('متن درباره ما'))


    def __str__(self):
        return self.content[:20]
    
    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))
    
    class Meta:
        verbose_name = _('متن درباره ما')
        verbose_name_plural = _('متن درباره ما')


class Employees(models.Model):
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=500)
    image = models.ImageField(upload_to='images/employees', verbose_name=_('عکس'))
    position = models.CharField(_('سمت'), max_length=300)

    def __str__(self):
        return f"{self.full_name} - {self.position}"
    
    class Meta:
        verbose_name = _('مشخصات کارمند')
        verbose_name_plural = _('مشخصات کارمندان')

    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))


class SliderHome(models.Model):
    title = models.CharField(_('عنوان اسلایدر'), max_length=350)
    image = models.ImageField(upload_to='images/slider', verbose_name=_('تصویر'))
    url = models.URLField(_('لینک'), null=True, blank=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))
    
    class Meta:
        verbose_name = _('اسلایدر')
        verbose_name_plural = _('اسلایدر')



class FooterBox(models.Model):
    name = models.CharField(max_length=300, verbose_name=_('نام'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('باکس فوتر')
        verbose_name_plural = _('باکس های فوتر')


class FooterLink(models.Model):
    footer_box = models.ForeignKey(FooterBox, on_delete=models.CASCADE, related_name='footer', verbose_name=_('باکس فوتر'))
    title = models.CharField(max_length=300, verbose_name=_('عنوان لینک'))
    url = models.URLField(_('لینک یو آر ال'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('لینک فوتر')
        verbose_name_plural = _('لینک های فوتر')
    

class Licence(CreateMixin):
    title = models.CharField(_('عنوان مجوز'), max_length=300)
    image = models.ImageField(upload_to='images/licence', verbose_name=_('عکس مجوز'))
    url = models.URLField(_('لینک مجوز'), null=True, blank=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.image.url))

    class Meta:
        verbose_name = _('مجوز')
        verbose_name_plural = _('مجوز ها')


class InformationShop(models.Model):
    telegram = models.URLField(_('تلگرام'), null=True, blank=True)
    instagram = models.URLField(_('اینستاگرام'), null=True, blank=True)
    whatsapp = models.URLField(_('واتساپ'), null=True, blank=True)
    email = models.URLField(_('ایمیل'), null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name=_('شماره تلفن'))
    address = models.CharField(_('آدرس'), max_length=500)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name = _('جزییات اطلاعات')
        verbose_name_plural = _('اطلاعات فروشگاه')
    

class Service(models.Model):
    icon = models.ImageField(upload_to='images/icon_service', verbose_name=_('آیکن'))
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    desc = models.CharField(max_length=250, verbose_name=_('توضیح خیلی کوتاه'))

    def __str__(self):
        return self.title
    
    def icon_tag(self):
        return format_html('<img src = "{}" width=60% height=40px>'.format(self.icon.url))
    
    class Meta:
        verbose_name = _('خدمات')
        verbose_name_plural = _('خدمات')

