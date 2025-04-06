from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import CreateMixin
from order.models import Order

User = get_user_model()


class Checkout(CreateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_checkout', verbose_name=_('سفارش'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_checkout', verbose_name=_('کاربر'))
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name=_('ایمیل(اختیاری)'))
    phone_number = models.CharField(max_length=11, verbose_name=_('شماره تلفن'))
    state = models.CharField(max_length=100, verbose_name=_('استان'))
    city = models.CharField(max_length=100, verbose_name=_('شهر'))
    zip_code = models.CharField(max_length=20, verbose_name=_('کد پستی'))
    address = models.CharField(max_length=300, verbose_name=_('آدرس'))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = _('مشخصات گیرنده')
        verbose_name_plural = _('مشخصات گیرندگان')
