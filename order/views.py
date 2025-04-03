from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.models import Product
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer



class PendingCartView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order, created = Order.objects.get_or_create(
            user=self.request.user,
            status=Order.StatusOrder.pending
        )
        return order


class AddToCartView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


    def create(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_id'])
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        mutable_data = request.data.copy()
        mutable_data['product'] = product.id

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.select_related('product', 'order')
    lookup_field = 'id'

    def perform_destroy(self, instance):
        order = instance.order
        super().perform_destroy(instance)

        if not order.order_item.exists():
            order.delete()


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": _("آیتم با موفقیت از سبد خرید حذف شد.")}, status=status.HTTP_200_OK)
    

class ClearCartView(generics.DestroyAPIView):
    """ حذف کامل سبد خرید"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def delete(self, request, *args, **kwargs):
        user = request.user
        with transaction.atomic():
            order = Order.objects.select_for_update().filter(user=user, status=Order.StatusOrder.pending).first()
            if not order:
                return Response({"detail": _("سبد خریدی یافت نشد.")}, status.HTTP_404_NOT_FOUND)

            order.delete()
            return Response({"detail": _("سبد خرید شما با موفقیت حذف شد.")}, status.HTTP_200_OK)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.select_related('user')
