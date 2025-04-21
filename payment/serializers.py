from rest_framework import serializers
from .models import Checkout


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'state', 'city', 'zip_code', 'address'
        ]

        