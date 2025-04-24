from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework import generics, permissions, serializers
from order.models import Order
from .models import Checkout
from .serializers import CheckoutSerializer



class CheckoutAPIView(generics.CreateAPIView):
    queryset = Checkout.objects.select_related('user', 'order')
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]


    @transaction.atomic()
    def perform_create(self, serializer):
        user = self.request.user

        try:
            order = Order.objects.select_for_update().get(user=user, status=Order.StatusOrder.pending)
        except Order.DoesNotExist:
                raise serializers.ValidationError({"detail": _("سبد خرید فعالی وجود ندارد.")})

        if not order.order_item.exists():
             raise serializers.ValidationError({"detail": _("سبد خرید شما خالی است.")})
        
        checkout = serializer.save(user=user, order=order)

        order.status = Order.StatusOrder.complete
        order.is_paid = True
        order.payment_date = timezone.now()
        order.save()

        return checkout
    