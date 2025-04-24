from rest_framework import serializers
from .models import Checkout


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = [
            'order', 'user', 'first_name', 'last_name', 'email', 'phone_number', 
            'state', 'city', 'zip_code', 'address'
        ]

        extra_fields = {
            'order': {'read_only': True},
            'user': {'read_only': True},
        }
        