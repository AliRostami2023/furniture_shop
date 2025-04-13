from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from product.models import Product


User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True, verbose_name=_('آیدی'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', verbose_name=_('کاربر'))

    class StatusOrder(models.TextChoices):
        pending = 'pending', _('در انتظار پرداخت')
        complete = 'complete', _('پرداخت شده')
        failed = 'failed', _('پرداخت ناموفق')

    status = models.CharField(max_length=20, choices=StatusOrder.choices, default=StatusOrder.pending, verbose_name=_('وضعیت سفارش'))
    total_price = models.IntegerField(default=0, verbose_name=_('قیمت کل سفارش'))
    payment_date = models.DateTimeField(_('تاریخ پرداخت'), null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name=_('پرداخت شده؟'))

    def __str__(self):
        return f"{self.user.full_name} - {self.status}"

    def get_total_price(self):
        total = self.order_item.aggregate(total_price=models.Sum(models.F(
                            'price') * models.F('quantity')))['total_price']
        return total or 0

    def save(self, *args, **kwargs):
        self.total_price = self.get_total_price()
        if self.total_price is None:
            self.total_price = 0
        super().save(*args, **kwargs)


    def update_total_price(self):
        self.total_price = sum(
            item.quantity * item.product.final_price()
            for item in OrderItem.objects.filter(order=self)
        )
        self.save()


    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارشات')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item', verbose_name=_('سفارش'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_item', verbose_name=_('محصول'))
    price = models.IntegerField(_('قیمت محصول'))
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_price()
    
    class Meta:
        verbose_name = _('جزییات سفارش')
        verbose_name_plural = _('جزییات سفارشات')
    