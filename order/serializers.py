from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem


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
                    'price': product.price,
                    'quantity': validated_data.get('quantity', 1)
                }
            )

            if not created:
                order_item.quantity += int(validated_data.get('quantity', 1))
                order_item.save()

            order.total_price += product.price * int(validated_data.get('quantity', 1))
            order.save()

            return order_item

    def destroy(self, instance):
        order = instance.order
        order.total_price -= instance.price * instance.quantity
        order.save()
        instance.delete()



class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_price', 'payment_date', 'is_paid', 'first_name', 'last_name',
            'email', 'phone_number', 'state', 'city', 'zip_code', 'address', 'order_item'
        ]
        read_only_fields = ['user', 'status', 'total_price', 'payment_date', 'is_paid'] 

    def total_price(self, obj):
        return obj.get_total_price()
