from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ListRetriveProductSerializer



class ViewOrderItemSerializer(serializers.ModelSerializer):
    product = ListRetriveProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity']
        read_only_fields = ['price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity']
        read_only_fields = ['price']


    def create(self, validated_data):
        user = self.context['request'].user

        with transaction.atomic():
            order, created = Order.objects.get_or_create(
                user=user,
                status=Order.StatusOrder.pending,
                defaults={'total_price': 0}
            )

            product = validated_data['product']
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    'price': product.final_price(),
                    'quantity': validated_data.get('quantity', 1)
                }
            )

            if not created:
                order_item.quantity += int(validated_data.get('quantity', 1))
                order_item.save()

            order.total_price += product.final_price() * int(validated_data.get('quantity', 1))
            order.save()

            return order_item

    def destroy(self, instance):
        order = instance.order
        order.total_price -= instance.final_price() * instance.quantity
        order.save()
        instance.delete()



class OrderSerializer(serializers.ModelSerializer):
    order_item = ViewOrderItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.full_name')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_price', 'payment_date', 'is_paid', 'order_item'
        ]
        read_only_fields = ['id', 'user', 'status', 'total_price', 'payment_date', 'is_paid'] 

    def total_price(self, obj):
        return obj.get_total_price()
