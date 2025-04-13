from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.models import Product
from .models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer, UpdateCartItemQuantityView



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


    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "محصول یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        quantity = int(request.data.get('quantity', 1))
        user = request.user

        with transaction.atomic():
            order, created = Order.objects.get_or_create(
                user=user,
                status=Order.StatusOrder.pending,
                defaults={'total_price': 0}
            )

            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    'price': product.final_price(),
                    'quantity': quantity
                }
            )

            if not created:
                order_item.quantity += quantity
                order_item.save()
            else:
                order_item.save()

            order.total_price += product.final_price() * quantity
            order.save()

            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class UpdateCartItemQuantityView(generics.UpdateAPIView):
    queryset = OrderItem.objects.prefetch_related('product', 'order')
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemQuantityView


    def patch(self, request, pk):
        try:
            order_item = OrderItem.objects.prefetch_related('order', 'product').get(id=pk, order__user=request.user, order__status=Order.StatusOrder.pending)
        except OrderItem.DoesNotExist:
            return Response({"detail": "آیتم مورد نظر در سبد خرید یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        try:
            new_quantity = int(request.data.get('quantity'))
            if new_quantity < 1:
                return Response({"detail": "تعداد باید حداقل ۱ باشد."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"detail": "تعداد معتبر وارد نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order_item.quantity = new_quantity
            order_item.save()
            order_item.order.update_total_price()

            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.select_related('product', 'order')
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        order = instance.order
        super().perform_destroy(instance)

        if not order.order_item.exists():
            order.delete()
        else:
            order.update_total_price()


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
        return Order.objects.filter(user=self.request.user, status=Order.StatusOrder.complete)
    


class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.select_related('user')
