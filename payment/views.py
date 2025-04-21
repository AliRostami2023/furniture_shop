from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, serializers
from .models import Checkout
from order.models import Order
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

        return checkout