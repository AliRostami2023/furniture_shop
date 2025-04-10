from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ListRetriveProductSerializer



class ViewOrderItemSerializer(serializers.ModelSerializer):
    product = ListRetriveProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity']
        read_only_fields = ['price']


class UpdateCartItemQuantityView(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']
        read_only_fields = ['id', 'order', 'product', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity']
        read_only_fields = ['price']



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
